resource "aws_iam_role_policy" "ec2_read_app_secret" {
  name = "${var.project_name}-read-app-secret"
  role = aws_iam_role.ec2_ssm.id

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [{
      Effect = "Allow"

      Action = [
        "secretsmanager:GetSecretValue"
      ]

      Resource = "arn:aws:secretsmanager:eu-central-1:442879245415:secret:tutorflow/app-*"
    }]
  })
}

# Secrets Manager entry for TutorFlow application credentials
resource "aws_secretsmanager_secret" "app" {
  name        = "${var.project_name}/app"
  description = "TutorFlow application PostgreSQL credentials"

  recovery_window_in_days = 7

  tags = {
    Name = "${var.project_name}-app-secret"
  }
}