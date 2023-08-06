import atexit
import sys
from typing import Any, Optional

import backoff
import numpy as np
import pandas as pd
from pydantic import BaseModel
import requests
from requests.models import Response

from terality.exceptions import _error_mapping
from terality.version import __version__
from .. import TeralityNetworkError, TeralityInternalError, TeralityError
from . import UploadConfig, DownloadConfig, TeralityConfig, logger, config_not_found, config_helper, TeralityCredentials


class _Process(BaseModel):
    """ Info about the python process using terality"""
    python_version_major: str = str(sys.version_info.major)
    python_version_minor: str = str(sys.version_info.minor)
    python_version_micro: str = str(sys.version_info.micro)
    numpy_version: str = np.__version__
    pandas_version: str = pd.__version__
    terality_version: str = __version__


class _Session(BaseModel):
    id: str
    upload_config: UploadConfig
    download_config: DownloadConfig


class ErrorResponse(BaseModel):
    type: Optional[str] = None
    message: str


def _is_non_retryable_code(e: requests.exceptions.RequestException) -> bool:
    # If we did not get a response, then always retry
    if not hasattr(e, "response") or e.response is None:
        return False
    # Retry on "too many requests"
    if e.response.status_code == 429:
        return False
    # 501 means "not implemented". Retrying won't help.
    if e.response.status_code == 501:
        return True
    # Otherwise, retry on any 500 error
    if e.response.status_code >= 500:
        return False
    # Otherwise, don't retry
    return True


class Connection:
    _config: TeralityConfig
    _credentials: TeralityCredentials
    _process: _Process = _Process()
    session: Optional[_Session] = None

    @classmethod
    def send_request(cls, action: str, payload: Any, without_session: bool = False) -> str:
        if cls._config is None:
            raise RuntimeError('Please specify user credentials')
        # Create new session on the fly if needed.
        if not without_session and cls.session is None:
            cls._create_session()

        try:
            r = cls._do_api_call(action, payload, without_session)
        except requests.HTTPError as e:
            server_error = ErrorResponse.parse_raw(e.response.text)
            error_class = _error_mapping.get(server_error.type, TeralityInternalError)
            trace_id = e.response.headers.get('X-Terality-Trace-Id')
            if trace_id is not None:
                raise error_class(f"{server_error.message} (request ID: {trace_id})")
            else:
                raise error_class(f"{server_error.message}")
        except requests.RequestException as e:
            raise TeralityNetworkError('Trouble contacting the API') from e
        except Exception as e:
            raise TeralityError('An unhandled error occurred when querying the API') from e

        return r.text

    @classmethod
    @backoff.on_exception(backoff.expo,
                          requests.exceptions.RequestException,
                          giveup=_is_non_retryable_code,
                          max_tries=5,
                          # Stop retries after 2 minutes.
                          # We assume that there is no value in automatically retrying
                          # calls after that, because one "/compute" or one "/follow_up" call should always
                          # return in less than 30 seconds, so we would have at least tried four times by that point.
                          max_time=120,
                          jitter=backoff.full_jitter)
    def _do_api_call(cls, action: str, payload: Any, without_session: bool = False) -> Response:
        full_url = f'{"https" if cls._config.use_https else "http"}://{cls._config.url}/{action}'
        r = requests.post(
            full_url,
            json={'session_id': None if without_session else cls.session.id, 'payload': payload},
            auth=(cls._credentials.user_id, cls._credentials.user_password),
            verify=cls._config.requests_ssl_verification,
            timeout=cls._config.timeout,
            headers=cls._process.dict(),
        )
        r.raise_for_status()
        return r

    @classmethod
    def _deserialize_session(cls, session_serialized: str) -> _Session:
        """ In a function rather than inline to allow monkey patching in tests"""
        return _Session.parse_raw(session_serialized)

    @classmethod
    def _create_session(cls) -> None:
        session_serialized = cls.send_request('create_session', None, without_session=True)
        cls.session = cls._deserialize_session(session_serialized)

    @classmethod
    def delete_session(cls) -> None:
        if cls.session is not None:
            cls.send_request('delete_session', {})
            cls.session = None

    @classmethod
    def set_up(cls, config: TeralityConfig, credentials: TeralityCredentials) -> None:
        cls._config = config
        cls._credentials = credentials
        cls._create_session()

    @classmethod
    def init(cls):
        if cls.session is None:
            logger.info('Initializing Terality')
            try:
                cls.set_up(TeralityConfig.load(), TeralityCredentials.load())
            except Exception as exc:
                logger.warning(exc)
                logger.warning(f'{config_not_found}\n{config_helper}')


def configure(user_id: str, user_password: str, *, check_connection: bool = True) -> None:
    """
    Provide Terality credentials and store them in the user's configuration directory.
    This also creates a configuration file if necessary.
    """
    credentials = TeralityCredentials(user_id=user_id, user_password=user_password)
    credentials.save()
    config = TeralityConfig.load(allow_missing=True)
    if config is None:
        config = TeralityConfig()
        config.save()
    if check_connection:
        Connection.set_up(config, credentials)


Connection.init()


def _atexit_delete_session():
    # Try to delete the current session, using a best effort policy. => Swallow any (Terality) exception.
    try:
        Connection.delete_session()
    except TeralityError:
        pass  # nosec: B110 (try_except_pass)


atexit.register(_atexit_delete_session)
