"""Tests unitarios para shared.config."""

from shared.config import Settings


def test_settings_defaults_without_endpoint() -> None:
    settings = Settings(_env_file=None)
    assert settings.environment == "dev"
    assert settings.aws_region == "us-east-1"
    assert settings.is_localstack is False


def test_settings_detects_localstack_when_endpoint_is_set() -> None:
    settings = Settings(_env_file=None, aws_endpoint_url="http://localhost:4566")
    assert settings.is_localstack is True
    assert settings.aws_endpoint_url == "http://localhost:4566"


def test_settings_treats_blank_endpoint_as_none() -> None:
    settings = Settings(_env_file=None, aws_endpoint_url="   ")
    assert settings.aws_endpoint_url is None
    assert settings.is_localstack is False


def test_settings_normalizes_log_level() -> None:
    settings = Settings(_env_file=None, urbanmove_log_level=" debug ")
    assert settings.log_level == "DEBUG"
