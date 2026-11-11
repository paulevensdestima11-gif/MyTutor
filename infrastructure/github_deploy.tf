

# Allow GitHub Actions to deploy TutorFlow through AWS Systems Manager

resource "aws_iam_role_policy" "github_actions_ssm_deploy" {
  name = "${var.project_name}-github-actions-ssm-deploy"
  role = aws_iam_role.github_actions_ecr.id

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ssm:SendCommand"
        ]
        Resource = [
          "arn:aws:ssm:eu-central-1::document/AWS-RunShellScript",
          "arn:aws:ec2:eu-central-1:442879245415:instance/i-03010727462391377"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "ssm:GetCommandInvocation"
        ]
        Resource = "*"
      }
    ]
  })
}
