from goaway import get_repository

r = get_repository()
f = r.package("main").file("main.go")

status = f.enum("Status", r.string)
with status as member:
    member("ok", "OK")
    member("ng", "NG")

with f.struct("Person") as field:
    field("Name", r.string, comment="person's name")
    field("Age", r.int)
    field("Father", f.structs["Person"].pointer)
    field("Mother", f.structs["Person"].pointer)

with f.struct("MorePerson") as field:
    field(f.structs["Person"])
    field("memo", r.string)

with f.interface("Greeter") as method:
    method("Greet", returns=r.string)

with f.interface("MoreGreeter", comment="hai") as method:
    method(f.interfaces["Greeter"])
    method("Greet2", returns=r.string)

# todo: embeded
print(r.writer.write(f, r.m))
