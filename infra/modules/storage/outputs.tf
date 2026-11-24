output "datalake_bucket_name" {
  description = "Nombre del bucket S3 del Data Lake."
  value       = aws_s3_bucket.datalake.bucket
}

output "datalake_bucket_arn" {
  description = "ARN del bucket S3 del Data Lake."
  value       = aws_s3_bucket.datalake.arn
}

output "processed_events_table_name" {
  description = "Nombre de la tabla DynamoDB para control de idempotencia."
  value       = aws_dynamodb_table.processed_events.name
}
