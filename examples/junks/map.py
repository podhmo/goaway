import goaway


r = goaway.get_repository()
foo = r.package("foo")
bar = r.package("bar")
f = r.file("bar.go")

print(r.int)
print(r.map(r.int, r.string), r.map(r.int, r.string)("m"), r.map(r.int, r.string)("m").typename(f))
print(r.map(foo.Foo, r.string), r.map(foo.Foo, r.string)("m"), r.map(foo.Foo, r.string)("m").typename(f))

print(r.chan(r.int).typename(f), r.chan(r.int, input=True).typename(f), r.chan(r.int, output=True).typename(f))
