from contextlib import contextmanager
from datetime import datetime
from uuid import uuid4

from papyru.logger import log_info


@contextmanager
def limited_runtime(timeout):
    start_time = datetime.now()

    def has_runtime_left():
        return (datetime.now() - start_time) < timeout

    try:
        yield has_runtime_left
    finally:
        pass


def parse_bool(value):
    if isinstance(value, bool):
        return value
    elif value is None:
        return False
    elif isinstance(value, str):
        return value.lower() in ('true', '1', 'yes')
    elif isinstance(value, int):
        return value == 1
    elif isinstance(value, float):
        return int(value) == 1
    else:
        raise TypeError('cannot parse bool from "%s".' % value)


def setup_request_ids():
    if setup_request_ids._already_patched:
        return
    else:
        setup_request_ids._already_patched = True

    import requests

    class PatchedSession(requests.sessions.Session):
        def prepare_request(self, request):
            request.headers = {**(request.headers or {}),
                               'pap-request-id': str(uuid4())}

            log_info('sending request %s: %s %s' % (
                request.headers.get('pap-request-id'),
                request.method,
                request.url))

            return super().prepare_request(request)

    requests.sessions.Session = PatchedSession


setup_request_ids._already_patched = False
