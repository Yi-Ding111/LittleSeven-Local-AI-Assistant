module "vpc" {
  source = "./vpc"

  cidr_block           = var.cidr_block
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
  tags                 = var.tags
}

module "iam" {
  source = "./iam"

  eks_cluster_role_name = var.eks_cluster_role_name
  eks_node_role_name    = var.eks_node_role_name
}


module "eks_cluster" {
  source = "./eks/eks-cluster-tf"

  eks_cluster_name     = var.eks_cluster_name
  eks_cluster_role_arn = module.iam.eks_cluster_role_arn
  eks_cluster_version  = var.eks_cluster_version
  eks_node_role_arn    = module.iam.eks_node_role_arn
  private_subnet_ids   = module.vpc.private_subnet_ids
  tags                 = var.tags
}
