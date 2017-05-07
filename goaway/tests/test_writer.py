import unittest
import textwrap


class WriterTests(unittest.TestCase):
    maxDiff = None

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

    def test_interface(self):
        r = self._getRepository()
        f = self._makeFile(r, "sort.go")

        # https://golang.org/src/sort/sort.go
        comment = textwrap.dedent(
            """
        A type, typically a collection, that satisfies sort.Interface can be
        sorted by the routines in this package. The methods require that the
        elements of the collection be enumerated by an integer index.
        """
        )
        Interface = f.interface("Interface", comment=comment.strip())

        len_comment = textwrap.dedent(
            """
        Len is the number of elements in the collection.
        """
        )
        Interface.define_method("Len", returns=f.int, comment=len_comment)

        less_comment = textwrap.dedent(
            """
        Less reports whether the element with
        index i should sort before the element with index j.
        """
        )
        Interface.define_method(
            "Less", args=(f.int("i"), f.int("j")), returns=f.bool, comment=less_comment
        )

        swap_comment = textwrap.dedent(
            """
        Swap swaps the elements with indexes i and j.
        """
        )
        Interface.define_method("Swap", args=(f.int("i"), f.int("j")), comment=swap_comment)

        actual = str(r.writer.write_interface(Interface, f, r.m))
        expected = textwrap.dedent(
            """
            // Interface : A type, typically a collection, that satisfies sort.Interface can be
            // sorted by the routines in this package. The methods require that the
            // elements of the collection be enumerated by an integer index.
            type Interface interface {
            	// Len is the number of elements in the collection.
            	Len() int
            	// Less reports whether the element with
            	// index i should sort before the element with index j.
            	Less(i int, j int) bool
            	// Swap swaps the elements with indexes i and j.
            	Swap(i int, j int)
            }
            """
        )
        self.assertEqual(actual.strip(), expected.strip())
