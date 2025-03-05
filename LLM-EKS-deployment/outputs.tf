output "private_subnet_ids" {
  description = "Private subnet ids in the VPC"
  value       = module.vpc.private_subnet_ids
}

output "eks_node_role_arn" {
  description = "The eks node role's ARN"
  value       = module.iam.eks_node_role_arn
}

output "eks_cluster_role_arn" {
  description = "The eks cluster role's ARN"
  value       = module.iam.eks_cluster_role_arn
}

output "eks_cluster_sg_id" {
  description = "EKS auto mode Security Group ID"
  value       = module.eks_cluster.eks_cluster_sg_id
}
