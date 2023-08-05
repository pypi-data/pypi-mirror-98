#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#
from typing import NamedTuple, Optional
from collections import defaultdict
import os
import sentry_sdk
import configparser
from pinecone.utils import get_version, get_environment

__all__ = ["CLIENT_VERSION", "Config", "PACKAGE_ENVIRONMENT", "SENTRY_DSN_TXT_RECORD"]

PACKAGE_VERSION = get_version()
PACKAGE_ENVIRONMENT = get_environment() or "development"
CLIENT_VERSION = "0.1"
SENTRY_DSN_TXT_RECORD = "pinecone-client.sentry.pinecone.io"


def _set_sentry_tags(config: dict):
    sentry_sdk.set_tag("package_version", PACKAGE_VERSION)
    for key, val in config.items():
        sentry_sdk.set_tag(key, val)


class ConfigBase(NamedTuple):
    environment: Optional[str] = None
    api_key: Optional[str] = None
    controller_host: Optional[str] = None
    hub_host: Optional[str] = None
    hub_registry: Optional[str] = None
    base_image: Optional[str] = None


class _CONFIG:
    """

    Order of configs to load:

    - configs specified explictly in reset
    - environment variables
    - configs specified in the INI file
    - default configs
    """

    def __init__(self):
        self.reset()

    def reset(self, config_file=None, **kwargs):
        config = ConfigBase()

        # Load config from file
        file_config = self._load_config_file(config_file)

        # Get the environment first. Make sure that it is not overwritten in subsequent config objects.
        environment = (
            kwargs.pop("environment", None)
            or os.getenv("PINECONE_ENVIRONMENT")
            or file_config.pop("environment", None)
            or "beta"
        )
        config = config._replace(environment=environment)

        # Set default config
        default_config = ConfigBase(
            controller_host="https://controller.{0}.pinecone.io".format(config.environment),
            hub_host="https://hub-api.{0}.pinecone.io".format(config.environment),
            hub_registry="https://hub.{0}.pinecone.io".format(config.environment),
            base_image="hub.{0}.pinecone.io/pinecone/base:{1}".format(config.environment, PACKAGE_VERSION),
        )
        config = config._replace(**self._filter_config(default_config._asdict()))

        # Set INI file config
        config = config._replace(**self._filter_config(file_config))

        # Set environment config
        env_config = ConfigBase(
            api_key=os.getenv("PINECONE_API_KEY"),
            controller_host=os.getenv("PINECONE_CONTROLLER_HOST"),
            hub_host=os.getenv("PINECONE_HUB_HOST"),
            hub_registry=os.getenv("PINECONE_HUB_REGISTRY"),
            base_image=os.getenv("PINECONE_BASE_IMAGE"),
        )
        config = config._replace(**self._filter_config(env_config._asdict()))

        # Set explicit config
        config = config._replace(**self._filter_config(kwargs))

        self._config = config

        # Sentry
        _set_sentry_tags(self._config._asdict())

    def _filter_config(self, config: dict) -> dict:
        """Retain only the valid keys and non-null values.

        Also removes the "environment" config from the config object.
        """
        return {
            key: val
            for key, val in config.items()
            if key != "environment" and key in ConfigBase._fields and val is not None
        }

    def _load_config_file(self, config_file: str) -> dict:
        """Load from INI config file."""
        config_obj = {}
        if config_file:
            full_path = os.path.expanduser(config_file)
            if os.path.isfile(full_path):
                parser = configparser.ConfigParser()
                parser.read(full_path)
                if "default" in parser.sections():
                    config_obj = {**parser["default"]}
        return config_obj

    @property
    def ENVIRONMENT(self):
        return self._config.environment

    @property
    def API_KEY(self):
        return self._config.api_key

    @property
    def CONTROLLER_HOST(self):
        return self._config.controller_host

    @property
    def HUB_HOST(self):
        return self._config.hub_host

    @property
    def HUB_REGISTRY(self):
        return self._config.hub_registry

    @property
    def BASE_IMAGE(self):
        return self._config.base_image


Config = _CONFIG()
