import logging

from .utils import convert_epoch_to_isoformat


__all__ = [
    'HumioJSONFormatter',
    'HumioKVFormatter',
]


class HumioKVFormatter(logging.Formatter):
    """Format a LogRecord into Humio kv format

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
        return ' '.join(f'{k}={v}' for k, v in kv.items())


class HumioJSONFormatter(logging.Formatter):
    """Format a LogRecord into Humio json format"""

    def format(self, record):
        timestamp = convert_epoch_to_isoformat(record.created)
        message = super().format(record)
        recorddict = vars(record)
        recorddict['asctime'] = timestamp
        recorddict['exc_info'] = repr(recorddict['exc_info'])
        recorddict['formattedMessage'] = message
        event = {
            'timestamp': timestamp,
            'attributes': recorddict,
            'rawstring': message,
        }
        blob = {'events': [event]}
        return blob
