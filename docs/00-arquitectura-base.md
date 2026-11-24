# Arquitectura Base — Sprint 0 (UrbanMove)

Este documento registra las decisiones fundacionales del **Sprint 0** para que los 3 integrantes
del equipo puedan desarrollar microservicios, Lambdas y aplicaciones cliente en paralelo con
criterios homogéneos de Clean Code, tolerancia a fallos y despliegue reproducible.

## 1. Arquitectura Limpia en 4 Capas

Cada microservicio en `services/<servicio>/` sigue una separación estricta de responsabilidades:

1. **`domain/`**: entidades, *value objects*, máquina de estados y excepciones de negocio (sin
   dependencias de FastAPI ni `boto3`).
2. **`application/`**: casos de uso (una operación por clase/función) y puertos (`typing.Protocol`).
3. **`infrastructure/`**: adaptadores reales (`DynamoDBRepository`, `SNSEventPublisher`) y
   adaptadores en memoria (`InMemory*`) para tests unitarios rápidos en CI.
4. **`api/`**: controladores FastAPI, DTOs Pydantic v2, inyección de dependencias y `/health`.

## 2. Patrones de Diseño Aplicados

- **Repository + Dependency Inversion (SOLID):** desacople entre casos de uso y DynamoDB.
- **Factory Method (`shared/`):** `EventFactory` garantiza el contrato de eventos y
  `AWSClientFactory` conmuta entre LocalStack (`dev`) y AWS Academy (`prod` con `LabRole`).
- **Pub-Sub + Idempotency Key:** SNS fan-out hacia colas SQS con DLQ (`maxReceiveCount = 3`) y
  deduplicación por `event_id` mediante `ProcessedEventsStore`.
- **State Pattern:** validará las transiciones legales de los 9 estados del vehículo en
  `availability` (Sprint 1).
- **Strategy Pattern:** cálculo de tarifas en `rides` y reglas de demanda en `relocation`.

## 3. Contrato de Eventos y Topología SNS/SQS

Todo evento publicado en el tópico `urbanmove-events` cumple el modelo inmutable `DomainEvent`:

- `event_id` (UUID v4)
- `timestamp` (ISO-8601 en UTC)
- `source` (microservicio productor)
- `event_type` (valor de `EventType`)
- `schema_version` (por defecto `"1.0"`)
- `correlation_id` (propagado vía `ContextVar` y cabecera HTTP)
- `payload` (`dict[str, Any]`)

```text
[Microservicios / Lambdas]
          │  SNSEventPublisher (MessageAttributes: event_type, source, correlation_id)
          ▼
   SNS: urbanmove-events
     ├──► SQS: urbanmove-history-dev              (todos los eventos) ──► DLQ (tras 3 fallos)
     ├──► SQS: urbanmove-analytics-ingest-dev     (todos los eventos) ──► DLQ (tras 3 fallos)
     ├──► SQS: urbanmove-maintenance-detector-dev (RideFinished, VehicleBatteryLow, IncidentReported) ──► DLQ
     └──► SQS: urbanmove-availability-sync-dev    (eventos de ciclo de vida) ──► DLQ
```

## 4. Data Lake y Almacenamiento Base

- **Bucket S3 `urbanmove-datalake-<env>`** con versionado activado y prefijos `raw/`, `trusted/`
  y `curated/`.
- **Tabla DynamoDB `urbanmove-processed-events-<env>`** (clave `event_id`, TTL `expires_at`) para
  garantizar idempotencia en consumidores y Lambdas.

## 5. Ejecución Local (Windows PowerShell y Linux/WSL)

En **Linux / macOS / WSL**:
```bash
make up
make tf-init && make tf-apply
make lint && make test
```

En **Windows PowerShell**:
```powershell
docker compose up -d --wait
terraform -chdir=infra/dev init
terraform -chdir=infra/dev apply -auto-approve
.\.venv\Scripts\Activate.ps1
ruff check . ; ruff format --check . ; pytest -m "not integration"
```
