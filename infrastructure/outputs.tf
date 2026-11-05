output "ecr_repository_url" {
  description = "URL of the TutorFlow ECR repository"
  value       = aws_ecr_repository.tutorflow.repository_url
}
