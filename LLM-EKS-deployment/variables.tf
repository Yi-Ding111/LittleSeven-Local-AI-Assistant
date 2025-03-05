variable "region" {
  description = "The AWS region"
  type        = string
  default     = "ap-southeast-2"
}

variable "llm_s3_name" {
  description = "The name of the s3 bucket"
  type        = string
  default     = "yi-cloud"
}

variable "cidr_block" {
  description = "The VPC cidr block range"
  type        = string
  default     = "192.168.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "The VPC's public subnets cidr block range"
  type        = list(string)
  default     = ["192.168.0.0/18", "192.168.64.0/18"]
}

variable "private_subnet_cidrs" {
  description = "The VPC's private subnets cidr block range"
  type        = list(string)
  default     = ["192.168.128.0/18", "192.168.192.0/18"]
}

variable "subnet_count" {
  description = "Number of subnets to create"
  type        = number
  default     = 4
}

variable "tags" {
  description = "A map of tags to be applied to all resources"
  type        = map(string)
  default = {
    Name = "llm-eks-vpc"
    env  = "DEV"
  }
}

variable "eks_cluster_role_name" {
  description = "The name of IAM role for EKS cluster"
  type        = string
  default     = "eksAutoModeClusterRole-YiDing"
}

variable "eks_node_role_name" {
  description = "The name of IAM role for EKS node"
  type        = string
  default     = "eksAutoModeNodeRole-YiDing"
}

variable "eks_cluster_name" {
  description = "Name of the EKS cluster"
  type        = string
  default     = "eks-auto-demo"
}

variable "eks_cluster_version" {
  description = "Kubernetes version for the EKS cluster"
  type        = string
  default     = "1.31"
}
