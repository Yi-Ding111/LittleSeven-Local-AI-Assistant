# list the eks cluster info 
data "aws_eks_cluster" "eks_auto_demo" {
  name = aws_eks_cluster.eks_auto_demo.name
}
