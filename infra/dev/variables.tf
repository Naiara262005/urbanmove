variable "aws_region" {
  description = "Region AWS obligatoria del proyecto."
  type        = string
  default     = "us-east-1"
}

variable "localstack_endpoint" {
  description = "Endpoint local de LocalStack."
  type        = string
  default     = "http://localhost:4566"
}

variable "datalake_bucket_name" {
  description = "Nombre del bucket S3 del Data Lake en dev."
  type        = string
  default     = "urbanmove-datalake-dev"
}
