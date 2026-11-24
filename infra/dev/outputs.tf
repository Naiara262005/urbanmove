output "events_topic_arn" {
  description = "ARN del topico SNS principal en LocalStack."
  value       = module.messaging.events_topic_arn
}

output "queue_urls" {
  description = "URLs de las colas SQS de consumidores en LocalStack."
  value       = module.messaging.queue_urls
}

output "dlq_urls" {
  description = "URLs de las Dead-Letter Queues en LocalStack."
  value       = module.messaging.dlq_urls
}

output "datalake_bucket_name" {
  description = "Nombre del bucket S3 del Data Lake."
  value       = module.storage.datalake_bucket_name
}

output "processed_events_table_name" {
  description = "Nombre de la tabla DynamoDB de idempotencia."
  value       = module.storage.processed_events_table_name
}
