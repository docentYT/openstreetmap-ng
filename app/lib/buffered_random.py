from base64 import urlsafe_b64encode
from io import BytesIO
from os import urandom

import cython

from app.models.types import StorageKey

_BUFFER_SIZE = 2 * 1024 * 1024  # 2 MB
_BUFFER = BytesIO()


@cython.cfunc
def _randbytes(n: cython.Py_ssize_t) -> bytes:
    assert n > 0, 'Buffered random must generate positive number of bytes'

    buffer = _BUFFER
    result: bytes = buffer.read(n)
    remaining: cython.Py_ssize_t = n - len(result)

    while remaining > 0:
        buffer.write(urandom(_BUFFER_SIZE))
        buffer.seek(0)
        read: bytes = buffer.read(remaining)
        result += read
        remaining -= len(read)

    return result


def buffered_randbytes(n: int) -> bytes:
    """Generate a secure random byte string of length n."""
    return _randbytes(n)


def buffered_rand_urlsafe(n: int) -> str:
    """Generate a secure random URL-safe string of length n."""
    return urlsafe_b64encode(_randbytes(n)).rstrip(b'=').decode()


def buffered_rand_storage_key(suffix: str = '') -> StorageKey:
    """Generate a secure random storage key."""
    return StorageKey(buffered_rand_urlsafe(16) + suffix)
