"""Patron Factory Method para clientes y recursos boto3 (LocalStack vs AWS)."""

from typing import Any, Literal

import boto3
from botocore.config import Config

from shared.config import Settings

AWSServiceName = Literal["s3", "dynamodb", "sns", "sqs"]

_LOCALSTACK_DUMMY_VALUE = "test"


class AWSClientFactory:
    """Crea clientes boto3 adaptados automaticamente a LocalStack o AWS real.

    - En dev (`aws_endpoint_url` definido): usa endpoint local, credenciales
      ficticias y `addressing_style=path` para S3.
    - En prod (AWS Academy): delega autenticacion a la cadena IAM (`LabRole`).
    """

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def _build_kwargs(self, service_name: AWSServiceName) -> dict[str, Any]:
        kwargs: dict[str, Any] = {"region_name": self._settings.aws_region}
        if self._settings.is_localstack:
            kwargs["endpoint_url"] = self._settings.aws_endpoint_url
            kwargs["aws_access_key_id"] = _LOCALSTACK_DUMMY_VALUE
            kwargs["aws_secret_access_key"] = _LOCALSTACK_DUMMY_VALUE
            if service_name == "s3":
                kwargs["config"] = Config(s3={"addressing_style": "path"})
        return kwargs

    def create_client(self, service_name: AWSServiceName) -> Any:
        """Crea un cliente boto3 de bajo nivel."""
        return boto3.client(service_name, **self._build_kwargs(service_name))

    def create_resource(self, service_name: Literal["s3", "dynamodb"]) -> Any:
        """Crea un recurso boto3 de alto nivel."""
        return boto3.resource(service_name, **self._build_kwargs(service_name))
