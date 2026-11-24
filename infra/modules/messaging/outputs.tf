output "events_topic_arn" {
  description = "ARN del topico SNS principal de eventos."
  value       = aws_sns_topic.events.arn
}

output "queue_urls" {
  description = "Mapa de URLs de las colas SQS de consumidores."
  value       = { for k, q in aws_sqs_queue.consumer : k => q.url }
}

output "queue_arns" {
  description = "Mapa de ARNs de las colas SQS de consumidores."
  value       = { for k, q in aws_sqs_queue.consumer : k => q.arn }
}

output "dlq_urls" {
  description = "Mapa de URLs de las Dead-Letter Queues."
  value       = { for k, q in aws_sqs_queue.dlq : k => q.url }
}
