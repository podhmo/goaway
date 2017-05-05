from goaway.repository import Repository
from goaway.writer import Writer


def get_repository(writer_cls=None):
    writer_cls = writer_cls or Writer
    return Repository(writer_cls)
