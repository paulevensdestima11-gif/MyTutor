# Main VPC
resource "aws_vpc" "tutorflow" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "${var.project_name}-vpc"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "tutorflow" {
  vpc_id = aws_vpc.tutorflow.id

  tags = {
    Name = "${var.project_name}-igw"
  }
}

# Public subnet for EC2
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.tutorflow.id
  cidr_block              = "10.20.1.0/24"
  availability_zone       = var.availability_zones[0]
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.project_name}-public-subnet"
  }
}

# Private subnet A for RDS
resource "aws_subnet" "private_a" {
  vpc_id            = aws_vpc.tutorflow.id
  cidr_block        = "10.20.11.0/24"
  availability_zone = var.availability_zones[0]

  tags = {
    Name = "${var.project_name}-private-subnet-a"
  }
}

# Private subnet B for RDS
resource "aws_subnet" "private_b" {
  vpc_id            = aws_vpc.tutorflow.id
  cidr_block        = "10.20.12.0/24"
  availability_zone = var.availability_zones[1]

  tags = {
    Name = "${var.project_name}-private-subnet-b"
  }
}

# Public route table
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.tutorflow.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.tutorflow.id
  }

  tags = {
    Name = "${var.project_name}-public-rt"
  }
}

# Associate public subnet with public route table
resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}
