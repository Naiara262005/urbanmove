"""Tests unitarios para AWSClientFactory (LocalStack vs AWS prod)."""

from unittest.mock import patch

from shared.aws.client_factory import AWSClientFactory
from shared.config import Settings


def test_client_factory_localstack_s3_uses_path_style() -> None:
    settings = Settings(
        _env_file=None,
        aws_region="us-east-1",
        aws_endpoint_url="http://localhost:4566",
    )
    factory = AWSClientFactory(settings)

    with patch("shared.aws.client_factory.boto3.client") as mock_client:
        factory.create_client("s3")

    mock_client.assert_called_once()
    args, kwargs = mock_client.call_args
    assert args == ("s3",)
    assert kwargs["region_name"] == "us-east-1"
    assert kwargs["endpoint_url"] == "http://localhost:4566"
    assert kwargs["config"].s3 == {"addressing_style": "path"}


def test_client_factory_prod_omits_endpoint_and_static_credentials() -> None:
    settings = Settings(_env_file=None, aws_region="us-east-1", aws_endpoint_url=None)
    factory = AWSClientFactory(settings)

    with patch("shared.aws.client_factory.boto3.client") as mock_client:
        factory.create_client("dynamodb")

    mock_client.assert_called_once_with("dynamodb", region_name="us-east-1")


def test_client_factory_create_resource_delegates_to_boto3() -> None:
    settings = Settings(_env_file=None, aws_region="us-east-1", aws_endpoint_url=None)
    factory = AWSClientFactory(settings)

    with patch("shared.aws.client_factory.boto3.resource") as mock_resource:
        factory.create_resource("dynamodb")

    mock_resource.assert_called_once_with("dynamodb", region_name="us-east-1")
