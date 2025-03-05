output "eks_cluster_sg_id" {
  description = "EKS auto mode Security Group ID"
  value       = data.aws_eks_cluster.eks_auto_demo.vpc_config[0].cluster_security_group_id
}