from functools import partial
from collections import defaultdict
from prestring.go import GoModule


class Writer:
    def __init__(self, module_factory=GoModule):
        self.modules = defaultdict(module_factory)  # module is prestring's module

    def write(self, file, m=None):
        m = m or self.modules[file.fullname]
        return self.write_file(file, m=m)

    def write_file(self, file, m):
        m.stmt(str(file.package))
        m.sep()

        def import_(fullname, as_=None, im=None, file=None):
            im(fullname, as_=as_)
            return file.import_(fullname, as_=as_)

        with m.import_group() as im:
            m.import_ = partial(import_, im=im, file=file)
            for ipackage in file.imported.values():
                im(ipackage.fullname, as_=ipackage.as_)

        for func in file.functions.values():
            self.write_function(func, m=m)
            m.sep()
        return m

    def write_function(self, function, m):
        m.append(str(function))
        m.stmt(" {")
        with m.scope():
            function.body(m)
        m.stmt("}")
        return m
