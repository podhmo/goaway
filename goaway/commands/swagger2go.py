import logging
import sys
from magicalimport import import_symbol
from dictknife import loading
from goaway import get_repository, tag
from prestring import go
from dictknife.jsonknife.accessor import access_by_json_pointer
"""
- conflict check
- required support
- multiple ref

support
- primitive struct
- primitive array
- self recursion
- enum
"""

MARKER_FILENAME = "x-go-filename"
MARKER_TYPE = "x-go-type"
MARKER_IS_POINTER = "x-go-pointer"


class Walker:
    DEFAULT_MAPPING = {
        "boolean": "bool",
        "string": "string",
        "number": "float64",
        "integer": "int64",
    }

    def __init__(self, doc, file, repository, mapping=None):
        self.doc = doc
        self.file = file
        self.repository = repository
        self.defined = {}  # ref -> name, todo: conflict
        self.nullable = {}  # ref
        self.type_mapping = mapping or self.DEFAULT_MAPPING

    def resolve_file(self, prop):
        if MARKER_FILENAME in prop:
            return self.file.package.file(prop[MARKER_FILENAME])
        else:
            return self.file

    def resolve_type(self, prop):
        # todo: implement
        typ = prop["type"]
        return getattr(self.file, self.type_mapping[typ])

    def resolve_tag(self, name):
        return tag(json=name)

    def walk(self, d, name):
        if MARKER_TYPE in d:
            package_name, name = d[MARKER_TYPE].rsplit(".", 1)
            package = self.resolve_file(d).import_(package_name)
            return getattr(package, name)
        elif "$ref" in d:
            return self.walk_ref(d["$ref"])
        elif d["type"] == "object":
            return self.walk_object(d, name=name)
        elif d["type"] == "array":
            return self.walk_array(d, name=name)
        else:
            typ = self.resolve_type(d)
            if self.has_enum(d):
                typ = self.walk_enum(d, typ, name=name)
            if self.is_pointer(d):
                typ = typ.pointer
            return typ

    def walk_all(self):
        for name, d in (self.doc.get("definitions") or {}).items():
            self.walk(d, name)

    def walk_object(self, d, name):
        name = go.goname(name)
        struct = self.resolve_file(d).struct(name, comment=d.get("description"))
        for name, prop in (d.get("properties") or {}).items():
            typ = self.walk(prop, name=name)
            if getattr(typ, "fullname", "") == struct.fullname:
                typ = typ.pointer
            struct.define_field(
                go.goname(name), typ, comment=prop.get("description"), tag=self.resolve_tag(name)
            )
        if self.is_pointer(d):
            struct = struct.pointer
        return struct

    def walk_array(self, d, name):
        typ = self.walk(d["items"], name=name)
        name = go.goname(name)
        array = self.resolve_file(d).newtype(
            go.goname(name), type=typ.slice, comment=d.get("description")
        )
        if self.is_pointer(d):
            array = array.pointer
        return array

    def walk_ref(self, ref):
        if ref in self.defined:
            return self.defined[ref]

        d = access_by_json_pointer(self.doc, ref[1:])
        self.nullable[ref] = self.is_pointer(d)
        name = ref.rsplit("/", 1)[-1]
        sentinel = self.defined[ref] = _Sentinel()
        typ = self.defined[ref] = self.walk(d, name=name)
        sentinel._configure(typ)
        return typ

    def walk_enum(self, d, typ, name):
        name = go.goname(name)
        enum = self.resolve_file(d).enum(name, typ, comment=d.get("description"))
        for x in d["enum"]:
            enum.define_member(x, x)
        return enum

    def has_enum(self, d):
        return d.get("enum")

    def is_pointer(self, d):
        return d.get(MARKER_IS_POINTER, False)


class _Sentinel:
    def __init__(self):
        self._value = object()

    def _configure(self, value):
        self._value = value

    @property
    def typename(self):
        return self.pointer.typename

    def __getattr__(self, name):
        if self._value is None:
            raise RuntimeError("not configured")
        return getattr(self._value, name)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("src", nargs="?", default=None)
    parser.add_argument("--format", choices=loading.get_formats(), default=None)
    parser.add_argument("--dst", default=sys.stdout, type=argparse.FileType("w"))
    parser.add_argument("--ref", default=None)
    parser.add_argument("--package", default=None)
    parser.add_argument("--file", default="main.go")
    parser.add_argument("--position", default=None)
    parser.add_argument("--walker", default="goaway.commands.swagger2go:Walker")
    parser.add_argument("--writer", default="goaway.writer:Writer")
    parser.add_argument("--emitter", default="goaway.emitter:Emitter")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    loading.setup()

    r = get_repository(
        writer_cls=import_symbol(args.writer),
        emitter_cls=import_symbol(args.emitter),
    )

    doc = loading.loadfile(args.src)
    package = r.package(args.package or "main")
    walker_cls = import_symbol(args.walker)
    walker = walker_cls(doc, package.file(args.file), r)
    if args.ref:
        walker.walk_ref(args.ref)
    else:
        walker.walk_all()

    d = r.resolve_package_path(args.position, package)
    r.emitter.emit_package(package, d=d)


if __name__ == "__main__":
    main()
