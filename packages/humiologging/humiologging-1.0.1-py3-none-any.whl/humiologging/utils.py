from datetime import datetime, timezone
import socket


__all__ = [
    'convert_epoch_to_isoformat',
    'get_host',
    'make_safe_for_json',
]


def convert_epoch_to_isoformat(epoch):
    dt = datetime.fromtimestamp(epoch, tz=timezone.utc)
    return dt.isoformat()


def get_host():
    name = socket.gethostname()
    try:
        addrs = socket.getaddrinfo(name, None, 0, socket.SOCK_DGRAM, 0,
                                   socket.AI_CANONNAME)
    except socket.error:
        return None

    fqdns = list()
    ips = list()
    for addr in addrs:
        ip = addr[4][0]
        fqdn = addr[3]
        if fqdn:
            fqdns.append(fqdn)
        if ip:
            ips.append(ip)
    if fqdns:
        return fqdns[0]
    return ips[0]


def make_safe_for_json(recorddict):
    PRIMITIVE_TYPES = (str, int, float, bool, type(None))
    for key, value in recorddict.items():
        if not isinstance(value, PRIMITIVE_TYPES):
            recorddict[key] = repr(value)
    return recorddict
