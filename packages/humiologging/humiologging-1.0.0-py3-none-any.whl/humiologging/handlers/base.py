import logging

from humiolib.HumioClient import HumioIngestClient

from ..formatters import HumioJSONFormatter
from ..utils import get_host


__all__ = [
    'HumioHandler',
    'HumioJSONHandler',
]


# If this is not here, we get the following exception courtesy of urllib3:
# RecursionError: maximum recursion depth exceeded while encoding a JSON object
# iff global loglevel is DEBUG
_logger = logging.getLogger('urllib3')
_logger.setLevel(logging.ERROR)
# humiolib uses requests, which uses urllib3


class BaseHumioHandler(logging.Handler):

    def __init__(self, humio_host, ingest_token, level=logging.NOTSET, tags=None, add_host_tag=None, **_):
        super().__init__(level=level)
        self.humio_host = humio_host
        self.ingest_token = ingest_token
        self.tags = tags
        if add_host_tag:
            if not tags:
                self.tags = {}
            self.tags['host'] = get_host() or 'unknown'
        self.connection = HumioIngestClient(base_url=self.humio_host, ingest_token=self.ingest_token)

    def emit(self, record):
        self.send_to_humio(record)

    def send_to_humio(self, record):
        raise NotImplementedError


class HumioHandler(BaseHumioHandler):
    """An exception log handler that sends unstructured logs to Humio

    Make sure to use a formatter that Humio can parse"""

    def send_to_humio(self, record):
        parser = getattr(self.formatter, 'parser', None)
        client = self.connection
        client.ingest_messages(
            messages=[self.format(record)],
            tags=self.tags,
            parser=parser,
        )


class HumioJSONHandler(BaseHumioHandler):
    """An exception log handler that sends Humio JSON format logs to Humio"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.formatter = HumioJSONFormatter()

    def send_to_humio(self, record):
        recordblob = self.format(record)
        if self.tags:
            recordblob['tags'] = self.tags
        client = self.connection
        client.ingest_json_data([recordblob])
