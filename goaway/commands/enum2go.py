import logging
from dictknife import loading
from goaway import get_repository
from magicalimport import import_symbol

logger = logging.getLogger(__name__)
DEFAULT_MAPPING = {
    "boolean": "bool",
    "string": "string",
    "number": "float",
    "integer": "int",
}


def resolve_type(prop, repository, mapping=DEFAULT_MAPPING):
    name = mapping[prop["type"]]
    return getattr(repository, name)


def walk(data, package, r):
    for filename, d in data.items():
        f = package.file(filename)
        for name, schema in d.items():
            typ = resolve_type(schema, r)
            comment = schema.get("description", "").split("\n", 1)[0]
            with f.enum(name, typ, comment=comment) as member:
                for name, prop in schema["enum"].items():
                    comment = prop.get("description", "").split("\n", 1)[0]
                    value = prop.get("value", name)
                    member(name, value, comment=comment)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("src", nargs="?", default=None)
    parser.add_argument("--package", default=None)
    parser.add_argument("--position", default=None)
    parser.add_argument("--writer", default="goaway.writer:Writer")
    parser.add_argument("--emitter", default="goaway.emitter:Emitter")

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    loading.setup()

    r = get_repository(
        writer_cls=import_symbol(args.writer),
        emitter_cls=import_symbol(args.emitter),
    )

    data = loading.loadfile(args.src)
    package = r.package(args.package or "main")
    walk(data, package, r)

    d = r.resolve_package_path(args.position, package)
    r.emitter.emit_package(package, d=d)


if __name__ == "__main__":
    main()
