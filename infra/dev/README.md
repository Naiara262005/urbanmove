# Infraestructura Dev (LocalStack)

Despliega en LocalStack (`http://localhost:4566`) los recursos base de UrbanMove reutilizando
los modulos compartidos de `infra/modules/`:

- **Mensajeria (`modules/messaging`):** topico SNS `urbanmove-events`, 4 colas SQS con politicas
  de filtrado por `event_type` y entrega directa (`raw_message_delivery = true`), y 4 Dead-Letter
  Queues (`maxReceiveCount = 3`).
- **Almacenamiento (`modules/storage`):** bucket S3 `urbanmove-datalake-dev` con versionado y
  zonas `raw/`, `trusted/`, `curated/`, mas la tabla DynamoDB `urbanmove-processed-events-dev`
  para idempotencia por `event_id`.

## Uso rapido

```bash
docker compose up -d --wait
terraform -chdir=infra/dev init
terraform -chdir=infra/dev plan
terraform -chdir=infra/dev apply -auto-approve
terraform -chdir=infra/dev output
```

Para destruir los recursos y detener LocalStack:

```bash
terraform -chdir=infra/dev destroy -auto-approve
docker compose down -v
```
