# UrbanMove

Sistema distribuido de movilidad urbana para bicicletas y patinetes eléctricos.
Proyecto final universitario desarrollado por un equipo de 3 personas sobre AWS Academy.

## Arquitectura en una frase

10 microservicios atómicos (FastAPI, Clean Architecture) que se comunican mediante eventos
(SNS + SQS + DLQ), 4 funciones Lambda para tareas programadas y analítica (data lake en S3,
Data Marts en DuckDB) y 3 interfaces ligeras (usuarios, mantenimiento y dashboard operativo).

## Requisitos

- Python 3.12+
- Docker y Docker Compose
- Terraform >= 1.6

## Puesta en marcha (dev, LocalStack)

```bash
cp .env.example .env          # ajusta valores si es necesario
python -m venv .venv && source .venv/bin/activate
make install                  # dependencias de desarrollo
make up                       # LocalStack en http://localhost:4566
make tf-init && make tf-apply # infraestructura base en LocalStack
make test                     # tests unitarios
```

`make help` lista todos los comandos disponibles.

## Estructura del monorepo

```
services/     Microservicios (uno por carpeta, cada uno con Dockerfile, API y tests)
lambdas/      Funciones Lambda
apps/         App de Usuarios, App de Mantenimiento y Dashboard Operativo
shared/       Código común: eventos, fábricas de clientes AWS, logging JSON, idempotencia
infra/
  modules/    Módulos Terraform reutilizables (dev y prod)
  dev/        LocalStack
  prod/       AWS Academy Sandbox (us-east-1, rol LabRole)
docs/         Documentación del proyecto
.github/      Pipelines de CI
```

## Reglas del proyecto

- Código, entidades y eventos en inglés; documentación en español.
- Cada microservicio sigue 4 capas: `domain`, `application`, `infrastructure`, `api`.
- Type hints completos, `ruff check` + `ruff format` y tests con `pytest`.
- Todo evento incluye `event_id`, `timestamp`, `source`, `event_type`, `schema_version`
  y `correlation_id`.
- **Nunca** se versionan credenciales, tokens ni secretos: todo va por variables de entorno
  (ver `.env.example`).

## Estado

| Sprint | Contenido | Estado |
|--------|-----------|--------|
| 0 | Monorepo, `shared/`, LocalStack, Terraform dev, CI | En curso |
| 1 | Primer microservicio completo (*Golden Template*) | Pendiente |
