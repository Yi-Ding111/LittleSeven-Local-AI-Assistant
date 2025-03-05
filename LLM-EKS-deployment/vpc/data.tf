# list all available zones through data source

data "aws_availability_zones" "available" {
  state = "available"
}

# ap-southeast-2a
# ap-southeast-2b
# ap-southeast-2c
