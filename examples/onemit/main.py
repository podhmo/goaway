import logging
from goaway import get_repository


def onemit(f, fname):
    print("gofmt -w {}".format(fname))


def run(package_path, position):
    r = get_repository()

    package = r.package(package_path)

    f = package.file("person.go")
    person = f.struct("person")
    person.define_field("name", f.string)

    f = package.file("group.go")
    group = f.struct("group")
    group.define_field("name", f.string)
    group.define_field("members", person.slice)

    d = r.resolve_package_path(position, package)
    r.emitter.emit_package(package, d=d, onemit=onemit)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", default=None)
    parser.add_argument("--position", default=None)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    run(args.package, args.position)


if __name__ == "__main__":
    main()
