provider "aws" {
  region  = "eu-central-1"
  profile = "AdministratorAccess-442879245415"

  default_tags {
    tags = {
      Project     = "TutorFlow"
      Environment = "Development"
      ManagedBy   = "Terraform"
    }
  }
}