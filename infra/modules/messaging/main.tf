resource "aws_sns_topic" "events" {
  name = var.topic_name

  tags = {
    Project     = "urbanmove"
    Environment = var.environment
  }
}

resource "aws_sqs_queue" "dlq" {
  for_each = var.consumers

  name                      = "urbanmove-${each.key}-dlq-${var.environment}"
  message_retention_seconds = 1209600 # 14 dias para analisis y reprocesado

  tags = {
    Project     = "urbanmove"
    Environment = var.environment
    Role        = "dlq"
  }
}

resource "aws_sqs_queue" "consumer" {
  for_each = var.consumers

  name                       = "urbanmove-${each.key}-${var.environment}"
  visibility_timeout_seconds = 60
  message_retention_seconds  = 345600 # 4 dias

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.dlq[each.key].arn
    maxReceiveCount     = var.max_receive_count
  })

  tags = {
    Project     = "urbanmove"
    Environment = var.environment
    Consumer    = each.key
  }
}

data "aws_iam_policy_document" "allow_sns_to_sqs" {
  for_each = var.consumers

  statement {
    sid     = "AllowSNSPublish"
    effect  = "Allow"
    actions = ["sqs:SendMessage"]

    principals {
      type        = "Service"
      identifiers = ["sns.amazonaws.com"]
    }

    resources = [aws_sqs_queue.consumer[each.key].arn]

    condition {
      test     = "ArnEquals"
      variable = "aws:SourceArn"
      values   = [aws_sns_topic.events.arn]
    }
  }
}

resource "aws_sqs_queue_policy" "consumer" {
  for_each = var.consumers

  queue_url = aws_sqs_queue.consumer[each.key].id
  policy    = data.aws_iam_policy_document.allow_sns_to_sqs[each.key].json
}

resource "aws_sns_topic_subscription" "consumer" {
  for_each = var.consumers

  topic_arn            = aws_sns_topic.events.arn
  protocol             = "sqs"
  endpoint             = aws_sqs_queue.consumer[each.key].arn
  raw_message_delivery = true

  filter_policy = length(each.value.event_types) > 0 ? jsonencode({
    event_type = each.value.event_types
  }) : null

  depends_on = [aws_sqs_queue_policy.consumer]
}
