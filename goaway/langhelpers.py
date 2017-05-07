from prestring.utils import reify  # NOQA


def nameof(fullname, name=None):
    return name or fullname.split("/", -1)[-1]


def tostring(v):
    if isinstance(v, (str, bytes)):
        return '"{}"'.format(repr(v)[1:-1])
    else:
        return str(v)
