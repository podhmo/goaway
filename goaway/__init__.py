from goaway.repository import Repository
from goaway.writer import Writer
from goaway.emitter import Emitter


def get_repository(writer_cls=None, emitter_cls=None):
    writer_cls = writer_cls or Writer
    emitter_cls = emitter_cls or Emitter
    return Repository(writer_cls, emitter_cls)
