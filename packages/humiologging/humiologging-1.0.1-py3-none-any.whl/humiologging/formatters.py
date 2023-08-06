import logging

from .utils import convert_epoch_to_isoformat, make_safe_for_json


__all__ = [
    'HumioJSONFormatter',
    'HumioKVFormatter',
]


class HumioKVFormatter(logging.Formatter):
    """Format a LogRecord into Humio unstructured kv format

    Avoid equals signs in the logmessage itself as that might be
    interpreted as another key value pair."""
    parser = 'kv'

    def format(self, record):
        formattedMessage = super().format(record)
        kv = vars(record)
        kv['timestamp'] = convert_epoch_to_isoformat(record.created)
        kv['asctime'] = kv['timestamp']
        kv['args'] = None if not kv['args'] else ','.join(kv['args'])
        kv['msg'] = repr(kv['msg'])
        kv['formattedMessage'] = repr(formattedMessage)
        kv = make_safe_for_json(kv)
        return ' '.join(f'{k}={v}' for k, v in kv.items())


class HumioJSONFormatter(logging.Formatter):
    """Format a LogRecord into Humio structured format

    If this is used with HumioJSONHandler, do not set a parser on the
    ingest_token. If it is used with another handler, set the parser to
    "json-for-action"."""

    def format(self, record):
        timestamp = convert_epoch_to_isoformat(record.created)
        message = super().format(record)
        recorddict = vars(record)
        recorddict['asctime'] = timestamp
        recorddict['formattedMessage'] = message
        if not recorddict['args']:
            recorddict['args'] = None
        recorddict = make_safe_for_json(recorddict)
        event = {
            'timestamp': timestamp,
            'attributes': recorddict,
            'rawstring': message,
        }
        blob = {'events': [event]}
        return blob
