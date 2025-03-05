variable "eks_cluster_name" {
  description = "Name of the EKS cluster"
  type = string
}

variable "eks_cluster_version" {
  description = "Kubernetes version for the EKS cluster"
  type        = string
}

variable "eks_node_role_arn" {
  description = "The eks node role's ARN"
  type        = string
}

variable "eks_cluster_role_arn" {
  description = "The eks cluster role's ARN"
  type        = string
}

variable "private_subnet_ids" {
  description = "Private subnet ids in the VPC"
  type        = list(string)
}

variable "tags" {
  description = "A map of tags to be applied to all resources"
  type        = map(string)
}
