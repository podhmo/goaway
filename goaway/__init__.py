from goaway.repository import Repository
from goaway.writer import Writer


def get_repository(writer=None):
    writer = writer or Writer()
    return Repository(writer)
