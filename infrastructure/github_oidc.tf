
# GitHub Actions identity provider
resource "aws_iam_openid_connect_provider" "github" {
  url = "https://token.actions.githubusercontent.com"

  client_id_list = [
    "sts.amazonaws.com"
  ]

  tags = {
    Name = "${var.project_name}-github-oidc"
  }
}

# Trust policy: only this repository's main branch
resource "aws_iam_role" "github_actions_ecr" {
  name = "${var.project_name}-github-actions-ecr-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [{
      Effect = "Allow"

      Principal = {
        Federated = aws_iam_openid_connect_provider.github.arn
      }

      Action = "sts:AssumeRoleWithWebIdentity"

      Condition = {
        StringEquals = {
          "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
          "token.actions.githubusercontent.com:sub" = "repo:paulevensdestima11-gif/MyTutor:ref:refs/heads/main"
        }
      }
    }]
  })

  tags = {
    Name = "${var.project_name}-github-actions-ecr-role"
  }
}

# Allow GitHub Actions to push images to TutorFlow ECR
resource "aws_iam_role_policy" "github_actions_ecr_push" {
  name = "${var.project_name}-github-actions-ecr-push"
  role = aws_iam_role.github_actions_ecr.id

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ecr:GetAuthorizationToken"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "ecr:BatchCheckLayerAvailability",
          "ecr:InitiateLayerUpload",
          "ecr:UploadLayerPart",
          "ecr:CompleteLayerUpload",
          "ecr:PutImage"
        ]
        Resource = aws_ecr_repository.tutorflow.arn
      }
    ]
  })
}

# Expose the role ARN for GitHub Actions configuration
output "github_actions_ecr_role_arn" {
  description = "IAM role assumed by GitHub Actions to push TutorFlow images to ECR"
  value       = aws_iam_role.github_actions_ecr.arn
}

