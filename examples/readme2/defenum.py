import goaway
from goaway.langhelpers import tostring

r = goaway.get_repository()
f = r.package("status").file("status.go")

status = f.enum("Status", r.string)
with status as member:
    member("ok", "OK")
    member("ng", "NG")

status = f.enum("Priority", r.int64)
with status as member:
    member("High", 1)
    member("Normal", 0)
    member("Low", -1)


if __name__ == "__main__":
    print(r.writer.write_enum(status, f, r.m))
    print(r.writer.write_enum(status, f, r.m))
