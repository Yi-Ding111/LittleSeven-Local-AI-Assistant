variable "eks_cluster_role_name" {
  description = "The name of IAM role for EKS cluster"
  type        = string
}

variable "eks_node_role_name" {
  description = "The name of IAM role for EKS node"
  type        = string
}
