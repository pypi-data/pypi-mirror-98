from io import BufferedIOBase, BytesIO
from operator import itemgetter
from warnings import warn

import requests

try:
    from requests_cache import CachedSession as MaybeCachedSession
except ImportError:  # pragma: no cover
    warn(
        "optional dependency requests_cache is not installed; cache options "
        "to Session() have no effect",
        RuntimeWarning,
    )
    from requests import Session as MaybeCachedSession


# Known keyword arguments for requests_cache.CachedSession
CACHE_KW = [
    "cache_name",
    "backend",
    "expire_after",
    "allowable_codes",
    "allowable_methods",
    "old_data_on_error",
    "location",
    "fast_save",
    "extension",
]


class Session(MaybeCachedSession):
    """:class:`requests.Session` subclass with optional caching.

    If :mod:`requests_cache` is installed, this class caches responses.

    Parameters
    ----------
    timeout : float
        Timeout in seconds, used for every request.

    Other parameters
    ----------------
    kwargs :
        Values for any attributes of :class:`requests.Session`, e.g.
        :attr:`~requests.Session.proxies`,
        :attr:`~requests.Session.stream`, or
        :attr:`~requests.Session.verify`.
    """

    def __init__(self, timeout=30.1, **kwargs):
        # Separate keyword arguments for CachedSession
        cache_kwargs = dict(
            filter(itemgetter(1), [(k, kwargs.pop(k, None)) for k in CACHE_KW])
        )

        if MaybeCachedSession is not requests.Session:
            # Using requests_cache.CachedSession

            # No cache keyword arguments supplied = don't use the cache
            disabled = not len(cache_kwargs.keys())

            if disabled:
                # Avoid creating any file
                cache_kwargs.setdefault("backend", "memory")

            super(Session, self).__init__(**cache_kwargs)

            # Overwrite value from requests_cache.CachedSession.__init__()
            self._is_cache_disabled = disabled
        elif len(cache_kwargs):  # pragma: no cover
            raise ValueError(
                f"Arguments have no effect without requests_session: {cache_kwargs}"
            )
        else:  # pragma: no cover
            # Plain requests.Session: no arguments
            super(Session, self).__init__()

        # Store timeout; not a property of requests.Session
        self.timeout = timeout

        # Addition keyword arguments must match existing attributes of requests.Session
        for name, value in kwargs.items():
            if hasattr(self, name):
                setattr(self, name, value)


class ResponseIO(BufferedIOBase):
    """Buffered wrapper for :class:`requests.Response` with optional file output.

    :class:`ResponseIO` wraps a :class:`requests.Response` object's 'content'
    attribute, providing a file-like object from which bytes can be :meth:`read`
    incrementally.

    Parameters
    ----------
    response : :class:`requests.Response`
        HTTP response to wrap.
    tee : binary, writable :py:class:`io.BufferedIOBase`, defaults to io.BytesIO()
        *tee* is exposed as *self.tee* and not closed explicitly.
    """

    def __init__(self, response, tee=None):
        self.response = response
        if tee is None:
            tee = BytesIO()
        # If tee is a file-like object or tempfile, then use it as cache
        if isinstance(tee, BufferedIOBase) or hasattr(tee, "file"):
            self.tee = tee
        else:
            # So tee must be str or os.FilePath
            self.tee = open(tee, "w+b")
        self.tee.write(response.content)
        self.tee.seek(0)

    def readable(self):
        return True

    def read(self, size=-1):
        """Read and return up to `size` bytes by calling ``self.tee.read()``."""
        return self.tee.read(size)
