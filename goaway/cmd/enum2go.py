import os.path
import logging
from prestring import go
from dictknife import loading
from goaway import get_repository
logger = logging.getLogger(__name__)

DEFAULT_MAPPING = {
    "boolean": "bool",
    "string": "string",
    "number": "float64",
    "integer": "int64",
}


def resolve_type(prop, repository, mapping=DEFAULT_MAPPING):
    name = mapping[prop["type"]]
    return getattr(repository, name)


def resolve(data, package, r):
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
    parser.add_argument("--position", default=".")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    loading.setup()
    data = loading.loadfile(args.src)
    r = get_repository()
    package = r.package(args.package or "main")
    resolve(data, package, r)

    if package.name != "main":
        d = os.path.join(args.position, package.name)
    else:
        d = args.position
    os.makedirs(d, exist_ok=True)
    for f in package.files.values():
        fpath = os.path.join(d, f.name)
        with open(fpath, "w") as wf:
            logger.info("write: %s", fpath)
            wf.write(str(r.writer.write(f)))


if __name__ == "__main__":
    main()
