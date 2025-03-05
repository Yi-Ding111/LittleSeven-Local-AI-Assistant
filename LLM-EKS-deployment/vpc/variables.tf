variable "cidr_block" {
  description = "The VPC cidr block range"
  type        = string
}

variable "tags" {
  description = "A map of tags to be applied to all resources"
  type        = map(string)
}

variable "public_subnet_cidrs" {
  description = "The VPC's public subnets cidr block range"
  type        = list(string)
}

variable "private_subnet_cidrs" {
  description = "The VPC's private subnets cidr block range"
  type        = list(string)
}

