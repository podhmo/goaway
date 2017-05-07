# todo: rename
import unittest


class ExternalPackageTests(unittest.TestCase):
    def _makeOne(self, name):
        from goaway import get_repository
        return get_repository().package(name)

    def test_package(self):
        fmt = self._makeOne("fmt")
        self.assertEqual(str(fmt), "package fmt")

    def test_callable(self):
        fmt = self._makeOne("fmt")
        self.assertEqual(str(fmt.Println("hello world")), 'fmt.Println("hello world")')

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
