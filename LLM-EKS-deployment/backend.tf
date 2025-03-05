terraform {
  backend "s3" {
    bucket = ""
    key    = ""
    region = ""
  }
}

# terraform init -backend-config="./state.config"