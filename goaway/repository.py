from collections import (
    OrderedDict,
    defaultdict,
)
from goaway.structure import Package


class Repository:
    def __init__(self, writer):
        self.writer = writer
        self.builtins = self.make_builtins()
        self.packages = OrderedDict()

    def __getattr__(self, name):
        return getattr(self.builtins, name)

    def make_builtins(self):
        b = Package("*builtins*", name="*builtins*", virtual=True)
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
        b.string = b.type("string")
        b.int = b.type("int")
        b.string = b.type("float")
        return b

    def package(self, fullname, name=None):
        if fullname not in self.packages:
            package = Package(fullname, name=name)
            self.packages[fullname] = package
        return self.packages[fullname]
