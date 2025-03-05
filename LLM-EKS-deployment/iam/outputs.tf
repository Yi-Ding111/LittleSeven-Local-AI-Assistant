output "eks_node_role_arn" {
  description = "The eks node role's ARN"
  value       = aws_iam_role.eks_auto_node_role.arn
}

output "eks_cluster_role_arn" {
  description = "The eks cluster role's ARN"
  value       = aws_iam_role.eks_auto_cluster_role.arn
}
