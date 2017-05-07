import unittest
import textwrap


class WriterTests(unittest.TestCase):
    def _getRepository(self):
        from goaway import get_repository
        return get_repository()

    def _makeFile(self, repository, name):
        return repository.package("main").file(name)

    def test_function(self):
        r = self._getRepository()
        f = self._makeFile(r, "main.go")

        @f.func("Add", args=(f.int("x"), f.int("y")), returns=f.int, comment="+")
        def Add(m):
            m.return_(m.format("{} + {}", Add.x, Add.y))

        actual = str(r.writer.write_function(Add, f, r.m))
        expected = textwrap.dedent(
            """
            // Add : +
            func Add(x int, y int) int {
            	return x + y
            }
            """
        )
        self.assertEqual(actual.strip(), expected.strip())

    def test_struct(self):
        r = self._getRepository()
        f = self._makeFile(r, "main.go")
        time = f.import_("time")

        Person = f.struct("Person", comment="人間")
        Person.define_field("Name", f.int)
        Person.define_field("BirthDay", time.type("Time"))

        actual = str(r.writer.write_struct(Person, f, r.m))
        expected = textwrap.dedent(
            """
            // Person : 人間
            type Person struct {
            	Name int
            	BirthDay time.Time
            }
            """
        )
        self.assertEqual(actual.strip(), expected.strip())
