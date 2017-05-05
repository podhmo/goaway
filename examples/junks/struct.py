from goaway import get_repository

r = get_repository()
f = r.package("main").file("main.go")

with f.struct("Person") as field:
    field("Name", r.string, comment="person's name")
    field("Age", r.int)
    field("Father", f.structs["Person"].pointer)
    field("Mother", f.structs["Person"].pointer)

with f.interface("Greeter", comment="hai") as method:
    method("Greet", returns=r.string)

# todo: embeded
print(r.writer.write(f, r.m))
