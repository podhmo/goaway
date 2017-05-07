import os.path
import logging
logger = logging.getLogger(__name__)


class Emitter:
    def __init__(self, repository):
        self.repository = repository

    def emit_package(self, package, d=None):
        return dumptree(self.repository.writer, package, d=d)

    emit = emit_package


def dumptree(writer, package, d=None):
    d = d or package.filepath
    os.makedirs(d, exist_ok=True)
    for f in package.files.values():
        fpath = os.path.join(d, f.name)
        with open(fpath, "w") as wf:
            logger.info("write: %s", fpath)
            wf.write(str(writer.write(f)))
