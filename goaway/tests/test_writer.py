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
        \treturn x + y
        }
"""
        )
        self.assertEqual(actual.strip(), expected.strip())
