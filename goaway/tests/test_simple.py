# todo: rename
import unittest


class ExternalPackageTests(unittest.TestCase):
    def _makeOne(self, name, as_=None):
        from goaway import get_repository
        return get_repository().package(name, as_)

    def test_package(self):
        fmt = self._makeOne("fmt")
        self.assertEqual(str(fmt), "package fmt")

    def test_callable(self):
        fmt = self._makeOne("fmt")
        self.assertEqual(str(fmt.Println("hello world")), 'fmt.Println("hello world")')

    def test_callable2(self):
        fmt = self._makeOne("fmt", as_="my")
        self.assertEqual(str(fmt.Println("hello world")), 'my.Println("hello world")')

    def test_callable_nested(self):
        fmt = self._makeOne("fmt")
        self.assertEqual(
            str(fmt.Printf("hello %s", fmt.Sprintf("%s\n", "world"))),
            'fmt.Printf("hello %s", fmt.Sprintf("%s\\n", "world"))'
        )

    def test_callable_nested2(self):
        fmt = self._makeOne("fmt")
        my = self._makeOne("my")
        self.assertEqual(
            str(fmt.Printf("%d + %d = %d\n", 1, 1, my.Add(1, 1))),
            str('fmt.Printf("%d + %d = %d\\n", 1, 1, my.Add(1, 1))'),
        )

    def test_type(self):
        time = self._makeOne("time")
        self.assertEqual(str(time.type("Time")), "time.Time")

    def test_variable(self):
        time = self._makeOne("time")
        self.assertEqual(str(time.type("Time")("x")), "x")


class DefineStructTests(unittest.TestCase):
    def _makeFile(self, name, package="main", as_=None):
        from goaway import get_repository
        return get_repository().package(package, as_).file(name)

    def _makeOne(self, file, name):
        return file.struct(name)

    def test_type(self):
        file = self._makeFile("main.go")
        Person = self._makeOne(file, "Person")
        self.assertEqual(str(Person), "main.Person")

    def test_type_with_file(self):
        file = self._makeFile("main.go")
        Person = self._makeOne(file, "Person")
        self.assertEqual(str(Person.typename(file)), "Person")

    def test_type_with_file2(self):
        file = self._makeFile("main.go")
        file2 = self._makeFile("foo.go", package="github.com/foo/foo")
        Person = self._makeOne(file2, "Person")
        self.assertEqual(str(Person.typename(file)), "foo.Person")

    def test_type_with_file3(self):
        file = self._makeFile("main.go")
        file2 = self._makeFile("foo.go", package="github.com/foo/foo", as_="my")
        Person = self._makeOne(file2, "Person")
        self.assertEqual(str(Person.typename(file)), "my.Person")

    def test_variable(self):
        file = self._makeFile("main.go")
        Person = self._makeOne(file, "Person")
        p = Person("p")
        self.assertEqual(str(p), "p")
        self.assertEqual(str(p.typename(file)), "Person")
        self.assertEqual(str(p.withtype(file)), "p Person")

    def test_variable__pointer(self):
        file = self._makeFile("main.go")
        Person = self._makeOne(file, "Person")
        p = Person.pointer("p")
        self.assertEqual(str(p), "p")
        self.assertEqual(str(p.typename(file)), "*Person")
        self.assertEqual(str(p.withtype(file)), "p *Person")

    def test_field_type(self):
        file = self._makeFile("main.go")
        Person = self._makeOne(file, "Person")
        Person.define_field("Name", file.string)
        self.assertEqual(str(Person.Name), "string")
        self.assertEqual(str(Person.Name.typename(file)), "string")
        self.assertEqual(str(Person.Name.withtype(file)), "string string")  # xxx

    def test_field_type__with_self(self):
        file = self._makeFile("main.go")
        Person = self._makeOne(file, "Person")
        Person.define_field("Father", Person.pointer)
        self.assertEqual(str(Person.Father), "main.Person")
        self.assertEqual(str(Person.Father.typename(file)), "*Person")
        self.assertEqual(str(Person.Father.withtype(file)), "Person *Person")  # xxx

    def test_field_type__with_external_package(self):
        file = self._makeFile("main.go")
        time = file.import_("time")
        Person = self._makeOne(file, "Person")
        Person.define_field("BirthDay", time.type("Time"))
        self.assertEqual(str(Person.BirthDay), "time.Time")
        self.assertEqual(str(Person.BirthDay.typename(file)), "time.Time")
        self.assertEqual(str(Person.BirthDay.withtype(file)), "Time time.Time")  # xxx

    def test_field_variable(self):
        file = self._makeFile("main.go")
        Person = self._makeOne(file, "Person")
        Person.define_field("Name", file.string)
        p = Person("p")
        self.assertEqual(str(p.Name), "p.Name")  # xxx
        self.assertEqual(str(p.Name.typename(file)), "p.Name")  # xxx
        self.assertEqual(str(p.Name.withtype(file)), "p.Name p.Name")  # xxx

    def test_field_variable__with_external_package(self):
        file = self._makeFile("main.go")
        time = file.import_("time")
        Person = self._makeOne(file, "Person")
        Person.define_field("BirthDay", time.type("Time"))
        p = Person("p")
        self.assertEqual(str(p.BirthDay), "p.BirthDay")  # xxx
        self.assertEqual(str(p.BirthDay.typename(file)), "p.BirthDay")  # xxx
        self.assertEqual(str(p.BirthDay.withtype(file)), "p.BirthDay p.BirthDay")  # xxx


class DefineEnumTests(unittest.TestCase):
    def _makeFile(self, name, package="main", as_=None):
        from goaway import get_repository
        return get_repository().package(package, as_).file(name)

    def _makeOne(self, file, name, type):
        return file.enum(name, type)

    def test_type(self):
        file = self._makeFile("main.go")
        Status = self._makeOne(file, "Status", file.int)
        self.assertEqual(str(Status), "main.Status")

    def test_type_with_file(self):
        file = self._makeFile("main.go")
        Status = self._makeOne(file, "Status", file.int)
        self.assertEqual(str(Status.typename(file)), "Status")

    def test_type_with_file2(self):
        file = self._makeFile("main.go")
        file2 = self._makeFile("foo.go", package="github.com/foo/foo")
        Status = self._makeOne(file2, "Status", file.int)
        self.assertEqual(str(Status.typename(file)), "foo.Status")

    def test_member_type(self):
        file = self._makeFile("main.go")
        Status = self._makeOne(file, "Status", file.int)
        Status.define_member("OK", 0)
        Status.define_member("NG", 1)
        self.assertEqual(str(Status.OK), "int")

    def test_variable(self):
        file = self._makeFile("main.go")
        Status = self._makeOne(file, "Status", file.int)
        s = Status("s")
        self.assertEqual(str(s), "s")
        self.assertEqual(str(s.typename(file)), "Status")
        self.assertEqual(str(s.withtype(file)), "s Status")

    def test_variable__pointer(self):
        file = self._makeFile("main.go")
        Status = self._makeOne(file, "Status", file.int)
        s = Status.pointer("s")
        self.assertEqual(str(s), "s")
        self.assertEqual(str(s.typename(file)), "*Status")
        self.assertEqual(str(s.withtype(file)), "s *Status")


class DefineFunctionTests(unittest.TestCase):
    def _makeFile(self, name, package="main", as_=None):
        from goaway import get_repository
        return get_repository().package(package, as_).file(name)

    def _makeOne(self, file, name, *args, **kwargs):
        return file.func(name, *args, **kwargs)

    def test_type(self):
        file = self._makeFile("main.go")
        Add = self._makeOne(file, "Add", args=(file.int("x"), file.int("y")), returns=file.int)
        self.assertEqual(str(Add), "func Add(x int, y int) int")

    def test_type_with_file(self):
        file = self._makeFile("main.go")
        Add = self._makeOne(file, "Add", args=(file.int("x"), file.int("y")), returns=file.int)
        self.assertEqual(str(Add.typename(file)), "func(int, int) int")

    def test_type_with_file2(self):
        file = self._makeFile("main.go")
        file2 = self._makeFile("foo.go", package="github.com/foo/foo")
        Add = self._makeOne(file2, "Add", args=(file.int("x"), file.int("y")), returns=file.int)
        self.assertEqual(str(Add.typename(file)), "func(int, int) int")

    def test_type_with_external_package(self):
        file = self._makeFile("main.go")
        Time = file.import_("time").type("Time")
        Add = self._makeOne(file, "Add", args=(Time("x"), Time("y")), returns=Time)
        self.assertEqual(str(Add.typename(file)), "func(time.Time, time.Time) time.Time")


class DefineInterfaceTests(unittest.TestCase):
    def _makeFile(self, name, package="main", as_=None):
        from goaway import get_repository
        return get_repository().package(package, as_).file(name)

    def _makeOne(self, file, name):
        return file.interface(name)

    def test_type(self):
        file = self._makeFile("main.go")
        Writer = self._makeOne(file, "Writer")
        self.assertEqual(str(Writer), "main.Writer")

    def test_type_with_file(self):
        file = self._makeFile("main.go")
        Writer = self._makeOne(file, "Writer")
        self.assertEqual(str(Writer.typename(file)), "Writer")

    def test_type_with_file2(self):
        file = self._makeFile("main.go")
        file2 = self._makeFile("foo.go", package="github.com/foo/foo")
        Writer = self._makeOne(file2, "Writer")
        self.assertEqual(str(Writer.typename(file)), "foo.Writer")

    def test_method_type(self):
        file = self._makeFile("main.go")
        Writer = self._makeOne(file, "Writer")
        Writer.define_method("Write", args=file.string("s"))
        self.assertEqual(str(Writer.Write), "func Write(s string)")
        self.assertEqual(str(Writer.Write.typename(file)), "func(string)")
        self.assertEqual(
            str(Writer.Write.typename(file, prefix=Writer.Write.name)), "Write(string)"
        )
        self.assertEqual(str(Writer.Write.withtype(file, prefix="")), " Write(s string)")  # xxx
