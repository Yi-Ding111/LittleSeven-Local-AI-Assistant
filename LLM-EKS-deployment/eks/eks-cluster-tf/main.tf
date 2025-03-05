resource "aws_eks_cluster" "eks_auto_demo" {
  name     = var.eks_cluster_name
  version  = var.eks_cluster_version
  role_arn = var.eks_cluster_role_arn

  bootstrap_self_managed_addons = false

  enabled_cluster_log_types = [
    "api",
    "audit",
    "authenticator",
    "controllerManager",
    "scheduler"
  ]

  access_config {
    authentication_mode = "API"
  }

  # compute resource config (auto mode)
  compute_config {
    enabled       = true
    node_pools    = ["system", "general-purpose"]
    node_role_arn = var.eks_node_role_arn
  }

  # VPC related configuration
  vpc_config {
    endpoint_private_access = true
    endpoint_public_access  = true
    subnet_ids              = var.private_subnet_ids # 包含所有私有子网
  }

  # ELB
  kubernetes_network_config {
    elastic_load_balancing {
      enabled = true
    }
  }

  # storage
  storage_config {
    block_storage {
      enabled = true
    }
  }


  # # ensure Iam roles needed are built up first
  # depends_on = [
  #   aws_iam_role_policy_attachment.eks_policies,
  #   aws_iam_role_policy_attachment.eks_node_policies
  # ]

  tags = var.tags
}

# add some addons
resource "aws_eks_addon" "vpc_cni" {
  cluster_name = aws_eks_cluster.eks_auto_demo.name
  addon_name   = "vpc-cni"
}

# resource "aws_eks_addon" "logging" {
#   cluster_name = aws_eks_cluster.eks_auto_demo.name
#   addon_name   = "amazon-cloudwatch-observability"
# }

# resource "aws_eks_addon" "metrics_server" {
#   cluster_name = aws_eks_cluster.eks_auto_demo.name
#   addon_name   = "metrics-server"
# }



data "aws_caller_identity" "current" {}

resource "aws_eks_access_entry" "eks_access_entry" {
  cluster_name  = aws_eks_cluster.eks_auto_demo.name
  principal_arn = data.aws_caller_identity.current.arn
  type          = "STANDARD"
}

resource "aws_eks_access_policy_association" "eks_access_policy_association" {
  cluster_name  = aws_eks_cluster.eks_auto_demo.name
  policy_arn    = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy"
  principal_arn = data.aws_caller_identity.current.arn
  access_scope {
    type = "cluster"
  }
}
