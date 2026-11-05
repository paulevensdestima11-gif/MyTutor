# RDS subnet group using our two private subnets
resource "aws_db_subnet_group" "tutorflow" {
  name = "${var.project_name}-db-subnet-group"

  subnet_ids = [
    aws_subnet.private_a.id,
    aws_subnet.private_b.id
  ]

  tags = {
    Name = "${var.project_name}-db-subnet-group"
  }
}

# PostgreSQL database
resource "aws_db_instance" "tutorflow" {
  identifier = "${var.project_name}-postgres"

  engine         = "postgres"
  instance_class = "db.t3.micro"

  allocated_storage = 20
  storage_type      = "gp3"
  storage_encrypted = true

  db_name  = "tutorflow"
  username = "tutorflow_admin"

  # AWS generates and manages the master password
  manage_master_user_password = true

  port = 5432

  db_subnet_group_name   = aws_db_subnet_group.tutorflow.name
  vpc_security_group_ids = [aws_security_group.rds.id]

  publicly_accessible = false
  multi_az            = false

  backup_retention_period    = 1
  auto_minor_version_upgrade = true

  deletion_protection = false
  skip_final_snapshot = true
  apply_immediately   = true

  tags = {
    Name = "${var.project_name}-postgres"
  }
}
