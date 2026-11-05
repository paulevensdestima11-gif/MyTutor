variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "tutorflow"
}

variable "vpc_cidr" {
  description = "CIDR block for the TutorFlow VPC"
  type        = string
  default     = "10.20.0.0/16"
}

variable "availability_zones" {
  description = "Availability Zones for private subnets"
  type        = list(string)
  default     = ["eu-central-1a", "eu-central-1b"]
}