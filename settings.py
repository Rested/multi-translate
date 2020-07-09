from enum import Enum
from pathlib import Path
from typing import Optional, List

import pydantic


class LogLevelEnum(Enum):
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"
    NOTSET = "NOTSET"


class FeaturesSettings(pydantic.BaseSettings):
    enable_persistence: bool = True
    enable_gql: bool = True
    # string as specified here https://limits.readthedocs.io/en/stable/string-notation.html
    # e.g. "10/minute;25/hour"
    rate_limits: Optional[str] = None
    redis_dsn: Optional[str] = None


class DatabaseSettings(pydantic.BaseSettings):
    postgres_dsn: pydantic.PostgresDsn
    db_connect_timeout_seconds: int = 10


class Settings(pydantic.BaseSettings):
    # logging
    log_level: LogLevelEnum = LogLevelEnum.INFO
    # microsoft
    microsoft_translator_subscription_key: Optional[str] = None
    microsoft_translator_endpoint: Optional[pydantic.HttpUrl] = None
    microsoft_translator_using_virtual_network: Optional[bool] = False
    microsoft_translator_region: Optional[str] = None
    # google
    google_svc_account_json_path: Optional[Path] = None
    google_parent_path: Optional[
        Path
    ] = None  # path of the project/location to apply the calls to
    google_endpoint: Optional[pydantic.HttpUrl] = pydantic.parse_obj_as(
        pydantic.HttpUrl, "https://translation.googleapis.com"
    )
    # yandex
    yandex_endpoint: Optional[pydantic.HttpUrl] = pydantic.parse_obj_as(
        pydantic.HttpUrl, "https://translate.api.cloud.yandex.net/translate/v2/"
    )
    yandex_iam_token: Optional[str] = None
    # applicable if using a yandex cloud user account to authorize
    yandex_folder_id: Optional[str] = None
    # papago
    # is it using Naver cloud (True) or Naver Developers (False)
    papago_naver_cloud: Optional[bool] = False
    papago_endpoint: Optional[pydantic.HttpUrl] = pydantic.parse_obj_as(
        pydantic.HttpUrl, "https://openapi.naver.com/v1/papago/n2mt"
    )
    papago_client_id: Optional[str] = None
    papago_client_secret: Optional[str] = None
    # amazon
    amazon_region: Optional[str] = None
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    # ibm watson
    # deep L
    deep_l_endpoint: Optional[pydantic.HttpUrl] = pydantic.parse_obj_as(
        pydantic.HttpUrl, "https://api.deepl.com/v2/"
    )
    deep_l_auth_key: Optional[str] = None
