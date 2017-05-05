from collections import defaultdict
from prestring.go import GoModule


class Writer:
    def __init__(self, module_factory=GoModule):
        self.modules = defaultdict(module_factory)  # module is prestring's module

    def write_file(self, file, m=None):
        m = m or self.modules[file.fullname]
        return file.write(m)
