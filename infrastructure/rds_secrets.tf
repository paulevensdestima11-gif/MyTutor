resource "aws_iam_role_policy" "ec2_read_rds_secret" {
  name = "${var.project_name}-read-rds-secret"
  role = aws_iam_role.ec2_ssm.id

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [{
      Effect = "Allow"

      Action = [
        "secretsmanager:GetSecretValue"
      ]

      Resource = aws_db_instance.tutorflow.master_user_secret[0].secret_arn
    }]
  })
}
