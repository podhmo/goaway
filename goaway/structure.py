import os.path
from collections import OrderedDict
from prestring import LazyFormat
from prestring.go import (
    goname,
    titlize,
)
from .langhelpers import (
    reify,
    nameof,
    tostring,
)


def string(value):
    return value.string()


def verbose_string(value):
    if hasattr(value, "verbose"):
        return value.verbose()
    else:
        return "<{value.__class__.__module__}.{value.__class__.__name__}: {!r}>".format(
            value.string(), value=value
        )


stringer_function = string


class Stringable:
    def __str__(self):
        return stringer_function(self)

    def new_instance(self, cls, *args, **kwargs):
        return cls(*args, **kwargs)


class Typeable:
    # self.name
    # self.package

    @property
    def shortname(self):
        return self.name[0].lower()

    def typename(self, file, typename=None):
        if file is None:
            return repr(self)  # buggy output
        if self.package.virtual or file.package.fullname == self.package.fullname:
            name = self.name
        else:
            name = "{}.{}".format(self.package.name, self.name)
        if typename is not None:
            name = typename.replace(self.name, name)
        return name

    @property
    def fullname(self):
        return "{}.{}".format(self.package.fullname, self.name)


class Valueable:
    # self.name
    # self.typename

    def value(self, name):
        return self.new_instance(Value, name, type=self)

    __call__ = value

    @reify
    def ref(self):
        return self.new_instance(Ref, self)

    @reify
    def pointer(self):
        return self.new_instance(Pointer, self)

    @reify
    def slice(self):
        return self.new_instance(Slice, self)

    def map(self, value):
        return self.new_instance(Map, self, value)

    def chan(self, input=False, output=False):
        return self.new_instance(Channel, self, input=input, output=output)

    channel = chan

    def withtype(self, file):
        return "{} {}".format(self.name, self.typename(file))


class Package(Stringable):
    def __init__(self, fullname, name=None, virtual=False):
        self.fullname = fullname
        self.name = nameof(fullname, name)
        self.virtual = virtual
        self.files = OrderedDict()

    def string(self):
        return "package {}".format(self.name)

    def verbose(self):
        return self.string()

    def __getattr__(self, name):
        v = self.symbol(name)
        setattr(self, name, v)
        return v

    @property
    def filepath(self):
        if self.virtual:
            return ""
        return os.path.join(os.getenv("GOPATH"), "src", self.fullname)

    def import_(self, fullname, name=None):
        return self.new_instance(ImportedPackage, fullname, name, package=self)

    def file(self, name):
        if name not in self.files:
            file = self.new_instance(File, name, package=self)
            self.files[name] = file
        return self.files[name]

    def type(self, name):
        return self.new_instance(Type, name, package=self)

    def symbol(self, name):
        return self.new_instance(Symbol, name, package=self)


class File(Stringable):
    def __init__(self, name, package):
        self.name = name
        self.package = package
        self.imported = OrderedDict()
        self.functions = OrderedDict()
        self.enums = OrderedDict()
        self.structs = OrderedDict()
        self.interfaces = OrderedDict()

    def string(self):
        return self.fullname

    @property
    def fullname(self):
        return os.path.join(self.package.filepath, self.name)

    def import_(self, fullname, as_=None):
        if fullname in self.imported:
            return self.imported[fullname]
        v = self.imported[fullname] = self.package.import_(fullname, name=as_)
        return v

    def enum(self, name, type, comment=None):
        name = goname(name)
        enum = self.new_instance(Enum, name, file=self, type=type, comment=comment)
        self.enums[name] = enum
        return enum

    def struct(self, name, comment=None):
        name = name
        struct = self.new_instance(Struct, name, file=self, comment=comment)
        self.structs[name] = struct
        return struct

    def interface(self, name, comment=None):
        name = name
        interface = self.new_instance(Interface, name, file=self, comment=comment)
        self.interfaces[name] = interface
        return interface

    def func(self, name, args=None, returns=None, body=None, comment=None, nostore=False):
        f = self.new_instance(
            Function, name, file=self, args=args, returns=returns, body=body, comment=comment
        )
        if not nostore:
            self.functions[name] = f
        return f

    def method(
        self, name, subject, args=None, returns=None, body=None, comment=None, nostore=False
    ):
        method = self.new_instance(
            Method, name, subject, args=args, returns=returns, body=body, comment=comment
        )
        if not nostore:
            self.functions[(subject.fullname, name)] = method
        return method


class ImportedPackage(Stringable):
    def __init__(self, fullname, name=None, package=None):
        self.fullname = fullname
        self.name = nameof(fullname, name)
        self.as_ = name
        self.package = package
        self.virtual = False

    def string(self):
        return self.fullname

    def verbose(self):
        return self.string()

    def type(self, name):
        return Type(name, package=self)

    def __getattr__(self, name):
        v = self.symbol(name)
        setattr(self, name, v)
        return v

    def symbol(self, name):
        return self.new_instance(Symbol, name, package=self)


class Type(Stringable, Typeable, Valueable):
    def __init__(self, name, package):
        self.name = name
        self.package = package

    def string(self):
        if self.package.virtual:
            return self.name
        return "{}.{}".format(self.package.name, self.name)


class Symbol(Type):
    def __call__(self, *args):
        return LazyFormat("{}({})", self.string(), ", ".join([tostring(e) for e in args]))


class Enum(Stringable, Typeable, Valueable):
    def __init__(self, name, type, file, comment=None):
        self.name = name
        self.type = type
        self.file = file
        self.comment = comment
        self.members = OrderedDict()

    def __enter__(self):
        return self.add_member

    def __exit__(self, type, value, tb):
        return None

    def string(self):
        if self.package.virtual:
            return self.name
        return "{}.{}".format(self.package.name, self.name)

    def verbose(self):
        return "<{}.{} name='{}.{}', type='{}', members={!r}>".format(
            self.__class__.__module__, self.__class__.__name__, self.file.package.name, self.name,
            self.type.string(), dict(self.members)
        )

    def add_member(self, name, value, comment=None):
        member = (name, value, comment)
        self.members[name] = member
        return member

    def varname(self, name):
        return goname("{}{}".format(self.name, titlize(name)))

    # typeable
    @property
    def package(self):
        return self.file.package


class Struct(Stringable, Typeable, Valueable):
    def __init__(self, name, file, comment=None):
        self.name = name
        self.file = file
        self.comment = comment
        self.fields = OrderedDict()

    def __enter__(self):
        return self.add_field

    def __exit__(self, type, value, tb):
        return None

    def string(self):
        if self.package.virtual:
            return self.name
        return "{}.{}".format(self.package.name, self.name)

    def verbose(self):
        return "<{}.{} name='{}.{}', type='{}'>".format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.file.package.name,
            self.name,
            self.type.string(),
        )

    def add_field(self, name, type=None, tag=None, comment=None):
        embeded = False
        if type is None:
            type = name
            name = type.name
            embeded = True

        field = (name, type, tag, comment, embeded)
        self.fields[name] = field
        return field

    def varname(self, name):
        return goname("{}{}".format(self.name, titlize(name)))

    # typeable
    @property
    def package(self):
        return self.file.package


class Interface(Stringable, Typeable, Valueable):
    def __init__(self, name, file, comment=None):
        self.name = name
        self.file = file
        self.comment = comment
        self.methods = OrderedDict()

    def __enter__(self):
        return self.add_method

    def __exit__(self, type, value, tb):
        return None

    def string(self):
        if self.package.virtual:
            return self.name
        return "{}.{}".format(self.package.name, self.name)

    def verbose(self):
        return "<{}.{} name='{}.{}', type='{}'>".format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.file.package.name,
            self.name,
            self.type.string(),
        )

    def add_method(self, name, args=None, returns=None, tag=None, comment=None):
        embeded = False
        if args is None and returns is None and not isinstance(name, (str, bytes)):
            f = name
            name = f.name
            embeded = True
        else:
            f = self.new_instance(Function, name, file=self.file, args=args, returns=returns)
        method = (name, f, tag, comment, embeded)
        self.methods[name] = method
        return method

    def varname(self, name):
        return goname("{}{}".format(self.name, titlize(name)))

    # typeable
    @property
    def package(self):
        return self.file.package


class Function(Stringable, Valueable):
    def __init__(self, name, file, args=None, returns=None, body=None, comment=None):
        self.name = name
        self.file = file
        self.args = None
        self.returns = None
        self.body = body
        self.comment = comment

        if args is not None:
            self.args = self.new_instance(Args, args, function=self)
        if returns is not None:
            self.returns = self.new_instance(Returns, returns, function=self)

    def __getattr__(self, name):
        for e in self.args or []:
            if e.name == name:
                setattr(self, name, e)
                return e
        for e in self.returns or []:
            if e.name == name:
                setattr(self, name, e)
                return e
        raise AttributeError(name)

    def __call__(self, *args):
        if self.body is None:
            self.body = args[0]  # dangerous!!!!!!
            return self
        else:
            return LazyFormat("{}({})", self.name, ", ".join([tostring(e) for e in args]))

    def string(self, prefix="func"):
        args = "" if self.args is None else self.args.withtype(self.file)
        returns = "" if self.returns is None else " {}".format(self.returns.withtype(self.file))
        return "{} {}({}){}".format(prefix, self.name, args, returns)

    def typename(self, file, prefix="func"):
        args = "" if self.args is None else self.args.typename(file)
        returns = "" if self.returns is None else " {}".format(self.returns.typename(file))
        return "{}({}){}".format(prefix, args, returns)


class Method(Function):
    def __init__(self, name, subject, args=None, returns=None, body=None, comment=None):
        self.subject = subject
        super().__init__(name, subject.file, args=args, returns=returns, body=body, comment=comment)

    def string(self):
        file = self.file  # xxx:
        args = "" if self.args is None else self.args.withtype(file)
        returns = "" if self.returns is None else " {}".format(self.returns.withtype(file))
        return "func ({} {}) {}({}){}".format(
            self.subject.shortname, self.subject.typename(file), self.name, args, returns
        )


class Args(Stringable):
    def __init__(self, args, function):
        if not isinstance(args, (list, tuple)):
            args = [args]
        self.args = args
        self.function = function

    def __iter__(self):
        return iter(self.args)

    def string(self):
        return self.withtype(self.function.file)

    def typename(self, file):
        return ", ".join([e.typename(file) for e in self.args])

    def withtype(self, file):
        return ", ".join([e.withtype(file) for e in self.args])


class Returns(Stringable):
    def __init__(self, args, function):
        if not isinstance(args, (list, tuple)):
            args = [args]
        self.args = args
        self.function = function

    def __iter__(self):
        return iter(self.args)

    def string(self):
        return self.withtype(self.function.file)

    def typename(self, file):
        if not self.args:
            return ""
        elif len(self.args) == 1:
            return self.args[0].typename(file)
        else:
            return "({})".format(", ".join([e.typename(file) for e in self.args]))

    def withtype(self, file):
        return self.typename(file)  # xxx


class Value(Stringable, Valueable):
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def string(self):
        return self.name

    def verbose(self):
        return "<{}.{} name='{}', type='{}'>".format(
            self.__class__.__module__, self.__class__.__name__, self.name, self.type.string()
        )

    @property
    def fullname(self):
        return "{}.{}".format(self.type.fullname, self.name)

    def typename(self, file):
        return self.type.typename(file)

    @property
    def package(self):
        return self.type.package


class Ref(Stringable, Valueable):
    def __init__(self, v):
        self.v = v

    def __getattr__(self, name):
        return getattr(self.v, name)

    @property
    def deref(self):
        return self.v

    def typename(self, file):
        return "&{}".format(self.v.typename(file))


class Map(Stringable, Valueable):
    def __init__(self, k, v):
        self.k = k
        self.v = v

    def __getattr__(self, name):
        return getattr(self.k, name)  # xxx

    def string(self):
        return self.typename(None)

    def typename(self, file):
        return "map[{}]{}".format(self.k.typename(file), self.v.typename(file))


class Channel(Stringable, Valueable):
    def __init__(self, v, input=False, output=False):
        self.v = v
        self.input = input
        self.output = output

    def __getattr__(self, name):
        return getattr(self.v, name)  # xxx

    def string(self):
        return self.typename(None)

    def typename(self, file):
        prefix = "{}chan{}".format("<-" if self.input else "", "<-" if self.output else "")
        return "{} {}".format(prefix, self.v.typename(file))


class Pointer(Stringable, Valueable):
    def __init__(self, v):
        self.v = v

    def __getattr__(self, name):
        return getattr(self.v, name)

    @property
    def depointer(self):
        return self.v

    def typename(self, file):
        return "*{}".format(self.v.typename(file))


class Slice(Stringable, Valueable):
    def __init__(self, v):
        self.v = v

    def __getattr__(self, name):
        return getattr(self.v, name)

    @property
    def deslice(self):
        return self.v

    def typename(self, file):
        return "[]{}".format(self.v.typename(file))
