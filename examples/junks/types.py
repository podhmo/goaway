from goaway import get_repository


r = get_repository()
f = r.package("main").file("main.go")

print(r.int.slice)
