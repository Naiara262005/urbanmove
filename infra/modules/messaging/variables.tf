variable "environment" {
  description = "Nombre del entorno (dev, prod)."
  type        = string
}

variable "topic_name" {
  description = "Nombre del topico SNS principal de eventos de dominio."
  type        = string
  default     = "urbanmove-events"
}

variable "max_receive_count" {
  description = "Numero de intentos antes de enviar un mensaje fallido a la DLQ."
  type        = number
  default     = 3
}

variable "consumers" {
  description = "Mapa de consumidores SQS y lista de event_type permitidos (lista vacia = todos)."
  type = map(object({
    event_types = list(string)
  }))
}
