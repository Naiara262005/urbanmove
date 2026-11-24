resource "aws_s3_bucket" "datalake" {
  bucket        = var.datalake_bucket_name
  force_destroy = var.force_destroy

  tags = {
    Project     = "urbanmove"
    Environment = var.environment
    Layer       = "analytics-datalake"
  }
}

resource "aws_s3_bucket_versioning" "datalake" {
  bucket = aws_s3_bucket.datalake.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_object" "datalake_zones" {
  for_each = toset(["raw/", "trusted/", "curated/"])

  bucket  = aws_s3_bucket.datalake.id
  key     = each.value
  content = ""
}

resource "aws_dynamodb_table" "processed_events" {
  name         = "urbanmove-processed-events-${var.environment}"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "event_id"

  attribute {
    name = "event_id"
    type = "S"
  }

  ttl {
    attribute_name = "expires_at"
    enabled        = true
  }

  tags = {
    Project     = "urbanmove"
    Environment = var.environment
    Purpose     = "idempotency"
  }
}
