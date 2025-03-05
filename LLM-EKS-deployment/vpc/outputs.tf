output "private_subnet_ids" {
  description = "Private subnet ids in the VPC"
  value       = aws_subnet.private[*].id
}
