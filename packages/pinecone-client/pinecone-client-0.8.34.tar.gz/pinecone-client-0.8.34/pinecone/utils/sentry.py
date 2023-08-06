from loguru import logger
import dns.resolver
import sentry_sdk
import os
import json

from pinecone.constants import PACKAGE_ENVIRONMENT, SENTRY_DSN_TXT_RECORD


def sentry_decorator(func):
    def inner_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            init_sentry()
            sentry_sdk.capture_exception(e)
            raise

    inner_func.__doc__ = func.__doc__
    return inner_func


def init_sentry():
    """Init Sentry if necessary.

    The Sentry DSN is stored as a txt record.
    """
    if not sentry_sdk.Hub.current.client:
        logger.info("Sentry is not initialized.")
        # sentry is not initialized
        sentry_dsn = None
        try:
            dns_result = dns.resolver.resolve(SENTRY_DSN_TXT_RECORD, "TXT")
            for res in dns_result:
                sentry_dsn = json.loads(res.to_text())
                break
        except Exception:
            logger.warning("Unable to resolve Sentry DSN.")
        if sentry_dsn:
            debug = os.getenv("SENTRY_DEBUG") == "True"
            sentry_sdk.init(dsn=sentry_dsn, debug=debug, environment=PACKAGE_ENVIRONMENT, traces_sample_rate=0.1)
    return None
