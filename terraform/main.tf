terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1" # Región estándar
}

# Bucket de S3 para almacenar el Lago de Datos Transaccionales de PLD
resource "aws_s3_bucket" "pld_data_lake" {
  bucket        = "pld-analytics-data-lake-gustavo"
  force_destroy = true
}

# Asegurar el bucket con cifrado AES256 del lado del servidor (Hardening de Seguridad)
resource "aws_s3_bucket_server_side_encryption_configuration" "pld_s3_encryption" {
  bucket = aws_s3_bucket.pld_data_lake.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
