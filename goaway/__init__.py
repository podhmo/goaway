from goaway.repository import Repository
from goaway.writer import Writer
from goaway.emitter import Emitter


def get_repository(writer_cls=None, emitter_cls=None):
    writer_cls = writer_cls or Writer
    emitter_cls = emitter_cls or Emitter
    return Repository(writer_cls, emitter_cls)


def tag(**kwargs):
    items = sorted(kwargs.items())
    return '`{}`'.format(" ".join('{k}:"{v}"'.format(k=k, v=_tagvalue(v)) for k, v in items))


def _tagvalue(v):
    if isinstance(v, (list, tuple)):
        return ",".join(str(x) for x in v)
    else:
        return v
