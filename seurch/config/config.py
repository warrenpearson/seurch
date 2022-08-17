import logging
import os

import attr
import yaml

logger = logging.getLogger(__name__)


@attr.define
class AppDatabaseSettings:
    user: str
    password: str = attr.ib(repr=lambda x: "***")
    host: str
    port: int = attr.ib(converter=int)
    database: str


@attr.define
class SentrySettings:
    dsn: str


@attr.define
class HoneycombSettings:
    api_key: str
    dataset: str


@attr.define
class S3Settings:
    region: str
    bucket: str
    url_endpoint: str


@attr.define
class Settings:
    environment: str
    application_name: str
    app_database: AppDatabaseSettings
    sentry: SentrySettings
    honeycomb: HoneycombSettings
    s3: S3Settings

    @classmethod
    def from_yaml(cls, file_name: str = None) -> "Settings":
        """Returns a Settings instance from a YAML filed defaulting to ./config.yml."""
        if file_name is None:
            here = os.path.dirname(os.path.realpath(__file__))
            file_name = f"{here}/config.yml"

        with open(file_name, "r") as stream:
            try:
                config = yaml.load(stream, Loader=yaml.SafeLoader)
            except yaml.YAMLError as err:
                logger.error(err)
                raise err

        return cls(**config)

    def __attrs_post_init__(self):
        """Populates the nested fields with the corresponding sections in the YAML."""
        for name, field in attr.fields_dict(type(self)).items():
            if attr.has(field.type):
                section = field.type(**getattr(self, name))
                setattr(self, name, section)


config = Settings.from_yaml()
