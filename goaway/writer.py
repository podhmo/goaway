from functools import partial
from collections import defaultdict
from prestring.go import (
    GoModule,
    goname,
    titlize,
)
from .langhelpers import tostring


class FileWriter:
    def __init__(self, writer):
        self.writer = writer

    def write(self, file, m):
        m.stmt(str(file.package))
        m.sep()

        def import_(fullname, as_=None, im=None, file=None):
            im(fullname, as_=as_)
            return file.import_(fullname, as_=as_)

        with m.import_group() as im:
            m.import_ = partial(import_, im=im, file=file)
            for ipackage in file.imported.values():
                im(ipackage.fullname, as_=ipackage.as_)

        for newtype in file.newtypes.values():
            self.writer.write_newtype(newtype, file, m=m)
            m.sep()
        for enum in file.enums.values():
            self.writer.write_enum(enum, file, m=m)
            m.sep()
        for interface in file.interfaces.values():
            self.writer.write_interface(interface, file, m=m)
            m.sep()
        for struct in file.structs.values():
            self.writer.write_struct(struct, file, m=m)
            m.sep()
        for f in file.functions.values():
            self.writer.write_function(f, file, m=m)
            m.sep()
        im.clear_ifempty()
        return m


class FuncWriter:
    def __init__(self, writer):
        self.writer = writer

    def write(self, f, file, m):
        if f.comment is not None or (f.name and f.name[0].isupper()):
            m.stmt('// {} : {}'.format(f.name, f.comment or ""))
        m.append(str(f))
        m.stmt(" {")
        with m.scope():
            f.body(m)
        m.stmt("}")
        return m


def _writecomment(m, prefix, comment):
    m.append(prefix)
    if not comment:
        m.stmt("")
        return
    lines = comment.strip().split("\n")
    m.stmt(lines[0])
    for line in lines[1:]:
        m.stmt("// {}", line)


class StructWriter:
    def __init__(self, writer):
        self.writer = writer

    def write(self, struct, file, m):
        if struct.comment is not None or (struct.name and struct.name[0].isupper()):
            _writecomment(m, '// {} : '.format(struct.name), struct.comment or "")
        with m.type_(struct.name, "struct"):
            for name, typ, tag, comment, embeded in struct.fields.values():
                if comment is not None and "\n" in comment:
                    _writecomment(m, '// ', comment)
                if embeded:
                    m.append(typ.typename(file))
                else:
                    m.append("{} {}".format(name, typ.typename(file)))
                if tag is not None:
                    m.append(" {}".format(tag))
                if comment is not None and "\n" not in comment:
                    m.append("  // {}".format(comment))
                m.stmt("")
        return m


class InterfaceWriter:
    def __init__(self, writer):
        self.writer = writer

    def write(self, interface, file, m):
        if interface.comment is not None or (interface.name and interface.name[0].isupper()):
            _writecomment(m, '// {} : '.format(interface.name), interface.comment or "")
        with m.type_(interface.name, "interface"):
            for name, f, tag, comment, embeded in interface.methods.values():
                if comment is not None and "\n" in comment:
                    _writecomment(m, '// ', comment)
                if embeded:
                    m.append(f.typename(file))
                else:
                    m.append(f.withtype(file, prefix=""))
                if tag is not None:
                    m.append(" {}".format(tag))
                if comment is not None and "\n" not in comment:
                    m.append("  // {}".format(comment))
                m.stmt("")
        return m


class NewtypeWriter:
    def __init__(self, writer):
        self.writer = writer

    def write(self, newtype, file, m):
        if newtype.comment is not None or (newtype.name and newtype.name[0].isupper()):
            _writecomment(m, '// {} : '.format(newtype.name), newtype.comment or "")
        m.type_alias(newtype.name, newtype.type.typename(file))
        return m


class EnumWriter:
    def __init__(self, writer):
        self.writer = writer

    @property
    def repository(self):
        return self.writer.repository

    def write(self, enum, file, m):
        self.write_definition(enum, file, m)
        self.write_string_method(enum, file, m)
        self.write_parse_method(enum, file, m)
        return m

    def write_definition(self, enum, file, m):
        m.stmt('// {} : {}'.format(enum.name, enum.comment or ""))
        m.stmt("type {} {}".format(enum.name, enum.type.typename(file)))
        m.sep()

        with m.const_group() as cm:
            for name, _, value, comment in enum.members.values():
                name = enum.varname(name)
                cm('// {} : {}'.format(name, comment or ""))
                cm('{} = {}({})'.format(name, enum.name, tostring(value)))

        return m

    def write_string_method(self, enum, file, m):
        r = self.repository
        fmt = m.import_("fmt")

        @file.method(
            "String", enum, returns=r.string, comment="stringer implementation", nostore=True
        )
        def string(m):
            s = enum.shortname
            with m.switch(s) as sw:
                for name, _, value, _ in enum.members.values():
                    with sw.case(enum.varname(name)):
                        sw.return_(tostring(name))
                with sw.default():
                    sw.stmt(
                        'panic({})'.format(
                            fmt.Sprintf(
                                "unexpected {} %s, in string()".format(enum.name),
                                _noencoded("string({})".format(s)),
                            )
                        )
                    )
            return m

        self.writer.write_function(string, file, m)

    def write_parse_method(self, enum, file, m):
        fmt = m.import_("fmt")

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
                for name, _, value, _ in enum.members.values():
                    with sw.case(tostring(value)):
                        sw.return_(enum.varname(name))
                with sw.default():
                    sw.stmt(
                        'panic({})'.format(
                            fmt.Sprintf(
                                "unexpected {} %v, in parse()".format(enum.name), _noencoded(s)
                            )
                        )
                    )
            return m

        self.writer.write_function(parse, file, m)


class Writer:
    file_writer_factory = FileWriter
    enum_writer_factory = EnumWriter
    newtype_writer_factory = NewtypeWriter
    struct_writer_factory = StructWriter
    interface_writer_factory = InterfaceWriter
    func_writer_factory = FuncWriter

    def __init__(self, repository, module_factory=GoModule):
        self.repository = repository
        self.modules = defaultdict(module_factory)  # module is prestring's module
        self.file_writer = self.file_writer_factory(self)
        self.enum_writer = self.enum_writer_factory(self)
        self.newtype_writer = self.newtype_writer_factory(self)
        self.struct_writer = self.struct_writer_factory(self)
        self.interface_writer = self.interface_writer_factory(self)
        self.func_writer = self.func_writer_factory(self)

    def write(self, file, m=None):
        m = m or self.modules[file.fullname]
        return self.write_file(file, m=m)

    def write_file(self, file, m):
        return self.file_writer.write(file, m)

    def write_enum(self, enum, file, m):
        return self.enum_writer.write(enum, file, m)

    def write_newtype(self, newtype, file, m):
        return self.newtype_writer.write(newtype, file, m)

    def write_struct(self, struct, file, m):
        return self.struct_writer.write(struct, file, m)

    def write_interface(self, interface, file, m):
        return self.interface_writer.write(interface, file, m)

    def write_function(self, f, file, m):
        return self.func_writer.write(f, file, m)


class _noencoded(object):
    def __init__(self, v):
        self.v = v

    def __str__(self):
        return self.v
