provider "aws" {
  region = "my-aws-region"
}

# IAM Role for AWS Services
resource "aws_iam_role" "aws_service_role" {
  name = "aws_service_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = ["glue.amazonaws.com", "quicksight.amazonaws.com"]
        },
      },
    ],
  })
}

# Attach necessary policies to the IAM role
resource "aws_iam_policy_attachment" "policy_attachment" {
  name       = "aws_service_role_policies"
  roles      = [aws_iam_role.aws_service_role.name]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

# S3 Bucket for Staging
resource "aws_s3_bucket" "staging_bucket" {
  bucket = "my-staging-bucket-name"
}

# S3 Bucket for Data Warehouse
resource "aws_s3_bucket" "data_warehouse_bucket" {
  bucket = "my-data-warehouse-bucket-name"
}

# AWS Glue Database
resource "aws_glue_catalog_database" "glue_database" {
  name = "glue_database"
}

# AWS Glue Crawler for Staging
resource "aws_glue_crawler" "glue_crawler" {
  name         = "glue_crawler"
  role         = aws_iam_role.aws_service_role.arn
  database_name = aws_glue_catalog_database.glue_database.name

  s3_target {
    path = aws_s3_bucket.staging_bucket.bucket
  }
}

# AWS Glue Job
resource "aws_glue_job" "glue_job" {
  name     = "glue_job"
  role_arn = aws_iam_role.aws_service_role.arn

  command {
    name            = "glueetl"
    script_location = "s3://${aws_s3_bucket.staging_bucket.bucket}/scripts/my_script.py"
    python_version  = "3"
  }

  default_arguments = {
    "--TempDir"             = "s3://${aws_s3_bucket.staging_bucket.bucket}/temp/"
    "--job-language"        = "python"
  }

  max_retries = 1
}

# Output for convenience
output "staging_bucket_name" {
  value = aws_s3_bucket.staging_bucket.bucket
}

output "data_warehouse_bucket_name" {
  value = aws_s3_bucket.data_warehouse_bucket.bucket
}

output "glue_crawler_name" {
  value = aws_glue_crawler.glue_crawler.name
}

output "glue_job_name" {
  value = aws_glue_job.glue_job.name
}
