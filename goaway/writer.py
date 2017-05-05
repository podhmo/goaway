from functools import partial
from collections import defaultdict
from prestring.go import (
    GoModule,
    goname,
    titlize,
)
from .langhelpers import tostring


class Writer:
    def __init__(self, repository, module_factory=GoModule):
        self.repository = repository
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

        for f in file.functions.values():
            self.write_function(f, file, m=m)
            m.sep()
        for enum in file.enums.values():
            self.write_enum(enum, file, m=m)
            m.sep()
        return m

    def write_function(self, f, file, m):
        if f.comment is not None or f.name[0].isupper():
            m.stmt('// {} : {}'.format(f.name, f.comment or ""))
        m.append(str(f))
        m.stmt(" {")
        with m.scope():
            f.body(m)
        m.stmt("}")
        return m

    def write_enum(self, enum, file, m):
        m.stmt('// {} : {}'.format(enum.name, enum.comment or ""))
        m.stmt("type {} {}".format(enum.name, enum.type.typename(file)))
        m.sep()
        with m.const_group() as cm:
            for name, value, comment in enum.members.values():
                name = enum.varname(name)
                cm('// {} : {}'.format(name, comment or ""))
                cm('{} = {}({})'.format(name, enum.name, tostring(value)))

        r = self.repository

        @file.method(
            "String", enum, returns=r.string, comment="stringer implementation", nostore=True
        )
        def string(m):
            s = enum.shortname
            with m.switch(s) as sw:
                for name, value, _ in enum.members.values():
                    with sw.case(enum.varname(name)):
                        sw.return_(tostring(name))
            return m

        @file.func(
            goname("Parse" + titlize(enum.name)),
            args=enum.type(enum.shortname),
            returns=enum,
            comment="parse",
            nostore=True
        )
        def parse(m):
            s = enum.shortname
            with m.switch(s) as sw:
                for name, value, _ in enum.members.values():
                    with sw.case(tostring(name)):
                        sw.return_(enum.varname(name))
            return m

        self.write_function(string, file, m)
        self.write_function(parse, file, m)
        return m
