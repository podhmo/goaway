import goaway


r = goaway.get_repository()
foo = r.package("foo")
bar = r.package("bar")
f = r.file("bar.go")

print(r.int)
print(r.int.map(r.string), r.int.map(r.string)("m"), r.int.map(r.string)("m").typename(f))
print(foo.Foo.map(r.string), foo.Foo.map(r.string)("m"), foo.Foo.map(r.string)("m").typename(f))

print(r.int.chan().typename(f), r.int.chan(input=True).typename(f), r.int.chan(output=True).typename(f))
