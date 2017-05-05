import os.path
from collections import (
    OrderedDict,
    defaultdict,
)
from prestring import LazyFormat
from prestring.go import GoModule


class reify(object):
    def __init__(self, wrapped):
        self.wrapped = wrapped
        try:
            self.__doc__ = wrapped.__doc__
        except:
            pass

    def __get__(self, inst, objtype=None):
        if inst is None:
            return self
        val = self.wrapped(inst)
        setattr(inst, self.wrapped.__name__, val)
        return val


def nameof(fullname, name=None):
    return name or fullname.split("/", -1)[-1]


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


class Typeaable:
    # self.name
    # self.package
    def value(self, name):
        return self.new_instance(Value, name, type=self)

    def typename(self, file, typename=None):
        if self.package.virtual or file.package.fullname == self.package.fullname:
            name = self.name
        else:
            name = "{}.{}".format(self.package.name, self.name)
        if typename is not None:
            name = typename.replace(self.name, name)
        return name

    __call__ = value


class Valueable:
    # self.name
    # self.typename
    @reify
    def ref(self):
        return self.new_instance(Ref, self)

    @reify
    def pointer(self):
        return self.new_instance(Pointer, self)

    @reify
    def slice(self):
        return self.new_instance(Slice, self)

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

    def string(self):
        return self.filepath

    @property
    def fullname(self):
        return os.path.join(self.package.filepath, self.name)

    def import_(self, fullname, as_=None):
        if fullname in self.imported:
            return self.imported[fullname]
        v = self.imported[fullname] = self.package.import_(fullname, name=as_)
        return v

    def enum(self, name, type, comment=None):
        enum = self.new_instance(Enum, name, file=self, type=type, comment=comment)
        self.enums[name] = enum
        return enum

    def func(self, name, args=None, returns=None, body=None, comment=None):
        function = self.new_instance(
            Function, name, file=self, args=args, returns=returns, body=body, comment=comment
        )
        self.functions[name] = function
        return function


class Enum(Stringable, Typeaable):
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

    # typeable
    @property
    def package(self):
        return self.file.package


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


class Type(Stringable, Typeaable):
    def __init__(self, name, package):
        self.name = name
        self.package = package

    def string(self):
        if self.package.virtual:
            return self.name
        return "{}.{}".format(self.package.name, self.name)

    @property
    def fullname(self):
        return "{}.{}".format(self.package.fullname, self.name)


class Symbol(Type):
    def __call__(self, *args):
        return LazyFormat("{}({})", self.string(), ", ".join([_encode(e) for e in args]))


def _encode(v):
    if isinstance(v, (str, bytes)):
        return '"{}"'.format(repr(v)[1:-1])
    else:
        return str(v)


class Function(Stringable, Valueable):
    def __init__(self, name, file, args=None, returns=None, body=None, comment=None):
        self.name = name
        self.file = file
        self._args = None
        self._returns = None
        self._body = body
        self.comment = comment

        if args is not None:
            self._args = self.new_instance(Args, args, function=self)
        if returns is not None:
            self._returns = self.new_instance(Returns, returns, function=self)

    def __getattr__(self, name):
        for e in self._args or []:
            if e.name == name:
                setattr(self, name, e)
                return e
        for e in self._returns or []:
            if e.name == name:
                setattr(self, name, e)
                return e
        raise AttributeError(name)

    def body(self, fn):
        self._body = fn  # xxx
        return self

    def __call__(self, *args):
        if self._body is None:
            return self.body(*args)  # dangerous!!!!!!
        else:
            return LazyFormat("{}({})", self.name, ", ".join([_encode(e) for e in args]))

    def string(self):
        args = "" if self._args is None else self._args.withtype(self.file)
        returns = "" if self._returns is None else " {}".format(self._returns.withtype(self.file))
        return "func {}({}){}".format(self.name, args, returns)

    def typename(self, file):
        args = "" if self._args is None else self._args.typename(file)
        returns = "" if self._returns is None else " {}".format(self._returns.typename(file))
        return "func({}){}".format(args, returns)


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

    def string(self):
        return "&{}".format(self.v.string())

    verbose = string

    def __getattr__(self, name):
        return getattr(self.v, name)

    @property
    def deref(self):
        return self.v

    depointer = deref

    def typename(self, file):
        return "&{}".format(self.v.typename(file))


class Pointer(Stringable, Valueable):
    def __init__(self, v):
        self.v = v

    def string(self):
        return "*{}".format(self.v.string())

    verbose = string

    def __getattr__(self, name):
        return getattr(self.v, name)

    @property
    def depointer(self):
        return self.v

    depointer = depointer

    def typename(self, file):
        return "*{}".format(self.v.typename(file))


class Slice(Stringable, Valueable):
    def __init__(self, v):
        self.v = v

    def string(self):
        return "[]{}".format(self.v.string())

    verbose = string

    def __getattr__(self, name):
        return getattr(self.v, name)

    def typename(self, file):
        return "[]{}".format(self.v.typename(file))

    def withtype(self, file, typename=None):
        return self.v.withtype(file=file, typename=typename or self.typename(file))


class Writer:
    def __init__(self, module_factory=GoModule):
        self.modules = defaultdict(module_factory)  # module is prestring's module

    def create_import_function(self, im, file):
        def import_(fullname, as_=None):
            im(fullname, as_=as_)
            return file.import_(fullname, as_=as_)

        return import_

    def _write_import_part(self, file, m):
        with m.import_group() as im:
            m.import_ = self.create_import_function(im, file)
            for ipackage in file.imported.values():
                im(ipackage.fullname, as_=ipackage.as_)

    def _write_function_part(self, file, m):
        for func in file.functions.values():
            m.append(str(func))
            m.stmt(" {")
            with m.scope():
                func._body(m)
            m.stmt("}")
            m.sep()

    def write_file(self, file, m=None):
        m = m or self.modules[file.fullname]
        m.stmt(str(file.package))
        m.sep()
        self._write_import_part(file, m)
        self._write_function_part(file, m)
        return m


def get_repository(writer=None):
    writer = writer or Writer()
    return Repository(writer)


class Repository:
    def __init__(self, writer):
        self.writer = writer
        self.builtins = self.make_builtins()
        self.packages = OrderedDict()

    def __getattr__(self, name):
        return getattr(self.builtins, name)

    def make_builtins(self):
        b = Package("*builtins*", name="*builtins*", virtual=True)
        b.int = b.type("int")
        b.string = b.type("string")
        return b

    def package(self, fullname, name=None):
        if fullname not in self.packages:
            package = Package(fullname, name=name)
            self.packages[fullname] = package
        return self.packages[fullname]
