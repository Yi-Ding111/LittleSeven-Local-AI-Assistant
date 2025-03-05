# build up vpc for llm eks
resource "aws_vpc" "eks-vpc" {
  cidr_block           = var.cidr_block
  enable_dns_hostnames = true
  enable_dns_support   = true

  # retrieves the value of a single element from a map
  tags = {
    Name = lookup(var.tags, "Name", "eks-vpc") # map, key, default value

  }
}


# build up public and private subnets
resource "aws_subnet" "public" {
  count             = length(var.public_subnet_cidrs)
  vpc_id            = aws_vpc.eks-vpc.id # binding with the defined vpc
  cidr_block        = var.public_subnet_cidrs[count.index]
  availability_zone = element(data.aws_availability_zones.available.names, count.index)
  # indicate that instances launched into the subnet should be assigned a public IP address
  map_public_ip_on_launch = true

  tags = {
    Name = "subnet-public-${count.index + 1}-${element(data.aws_availability_zones.available.names, count.index)}"
    # Let EKS recognize the Public Subnet that can be used to create an Internet-facing ELB
    "kubernetes.io/role/elb" = "1"
  }
}

resource "aws_subnet" "private" {
  count             = length(var.private_subnet_cidrs)
  vpc_id            = aws_vpc.eks-vpc.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = element(data.aws_availability_zones.available.names, count.index)

  tags = {
    Name = "subnet-private-${count.index + 1}-${element(data.aws_availability_zones.available.names, count.index)}"
    # Internal ELB in private subnet
    "kubernetes.io/role/internal-elb" = "1"
  }
}

# create an IGW, connect with exteral internet
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.eks-vpc.id

  tags = {
    Name = "${lookup(var.tags, "Name", "eks-vpc")}-igw"
  }
}


# apply elastic IPs for NAT gateway
resource "aws_eip" "nat_eip" {
  count = length(var.public_subnet_cidrs)
}

# create nat gateway for private subnets 
# to comminucate with internet (pull the image down)
resource "aws_nat_gateway" "nat" {
  count         = length(var.public_subnet_cidrs)
  allocation_id = aws_eip.nat_eip[count.index].id
  subnet_id     = aws_subnet.public[count.index].id

  tags = {
    Name = "eks-nat-gateway-${element(data.aws_availability_zones.available.names, count.index)}-${count.index + 1}"
  }
}


# create route table for public subnet
# Allow Public Subnet to access the public network
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.eks-vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "eks-public-route-table"
  }
}

# associate public route table with public subnets
# resource "aws_route_table_association" "public" {
#   for_each      = { for idx, subnet in aws_subnet.public : idx => subnet.id }
#     # {
#     # 0 = "subnet-0",
#     #1 = "subnet-1"
#     # }
#   subnet_id     = each.value
#   route_table_id = aws_route_table.public.id
# }
resource "aws_route_table_association" "public" {
  count          = length(var.public_subnet_cidrs)
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

# create route table for private subnet
# let private subnet access public internet to pull image through NAT nateway
resource "aws_route_table" "private" {
  count  = length(var.private_subnet_cidrs)
  vpc_id = aws_vpc.eks-vpc.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat[count.index].id
  }

  tags = {
    Name = "eks-private-route-table-${element(data.aws_availability_zones.available.names, count.index)}-${count.index + 1}"
  }
}

# associate private route table with private subnets
resource "aws_route_table_association" "private" {
  count          = length(var.private_subnet_cidrs)
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private[count.index].id
}


resource "aws_security_group" "eks_control_plane" {
  vpc_id      = aws_vpc.eks-vpc.id
  description = "EKS control plane security group"

  tags = {
    Name = "eks-control-plane-sg"
  }
}
