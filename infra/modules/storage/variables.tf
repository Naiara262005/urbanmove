variable "environment" {
  description = "Nombre del entorno (dev, prod)."
  type        = string
}

variable "datalake_bucket_name" {
  description = "Nombre del bucket S3 para el Data Lake (raw/trusted/curated)."
  type        = string
}

variable "force_destroy" {
  description = "Permite borrar el bucket aunque contenga objetos (util en dev y limpieza)."
  type        = bool
  default     = true
}
