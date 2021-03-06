import os.path
from collections import OrderedDict
from prestring.go import GoModule
from .structure import (
    Package,
    Map,
    Channel,
)
from .langhelpers import reify


class Repository:
    def __init__(self, writer_cls, emitter_cls):
        self.writer_cls = writer_cls
        self.emitter_cls = emitter_cls
        self.packages = OrderedDict()

    @reify
    def writer(self):
        return self.writer_cls(self)

    @reify
    def emitter(self):
        return self.emitter_cls(self)

    @reify
    def builtins(self):
        return make_builtins("*builtins*")

    @property
    def m(self):
        return GoModule()

    def resolve_package_path(self, d, package):
        if d is None:
            return package.filepath
        if package.name != "main":
            return os.path.join(d, package.name)
        else:
            return d

    def __getattr__(self, name):
        return getattr(self.builtins, name)

    def package(self, fullname, name=None):
        if fullname not in self.packages:
            package = Package(fullname, name=name, repository=self)
            self.packages[fullname] = package
        return self.packages[fullname]


def make_builtins(name):
    b = Package(name, name=name, virtual=True)
    b.bool = b.type("bool")
    b.string = b.type("string")
    b.int = b.type("int")
    b.int8 = b.type("int8")
    b.int16 = b.type("int16")
    b.int32 = b.type("int32")
    b.int64 = b.type("int64")
    b.uint = b.type("uint")
    b.uint8 = b.type("uint8")
    b.uint16 = b.type("uint16")
    b.uint32 = b.type("uint32")
    b.uint64 = b.type("uint64")
    b.uintptr = b.type("uintptr")
    b.byte = b.type("byte")
    b.rune = b.type("rune")
    b.float32 = b.type("float32")
    b.float64 = b.type("float64")
    b.complex64 = b.type("complex64")
    b.complex128 = b.type("complex128")
    b.map = Map
    b.chan = b.channel = Channel
    return b
