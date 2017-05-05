goaway
========================================

.. image:: https://travis-ci.org/podhmo/goaway.svg?branch=master
    :target: https://travis-ci.org/podhmo/goaway


example
----------------------------------------

main.py

.. code-block:: python

  import goaway
  
  r = goaway.get_repository()
  f = r.package("main").file("main.go")
  fmt = f.import_("fmt")
  
  
  @f.func("hello")
  def hello(m):
      m.stmt(fmt.Println("hello world"))
  
  
  @f.func("add", args=(r.int("x"), r.int("y")), returns=r.int)
  def add(m):
      m.return_("{} + {}".format(add.x, add.y))
  
  
  @f.func("main")
  def main(m):
      m.stmt(hello())
      m.stmt(fmt.Printf("1 + 2 = %d\n", add(1, 2)))
  
  
  if __name__ == "__main__":
      m = r.writer.write(f)
      print(m)


.. code-block:: bash

  python main.py > main.go
  goimports -w main.go
  go run main.go
  hello world
  1 + 2 = 3
  

main.go

.. code-block:: main.go

  package main
  
  import (
  	"fmt"
  )
  
  func hello() {
  	fmt.Println("hello world")
  }
  
  func add(x int, y int) int {
  	return x + y
  }
  
  func main() {
  	hello()
  	fmt.Printf("1 + 2 = %d\n", add(1, 2))
  }


example2
----------------------------------------

main.py

.. code-block:: python

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


.. code-block:: bash

  

struct.go

.. code-block:: struct.go

  package main
  
  import (
  	"fmt"
  )
  
  // Status :
  type Status string
  
  const (
  	// StatusOk :
  	StatusOk = Status("OK")
  	// StatusNg :
  	StatusNg = Status("NG")
  )
  
  // String : stringer implementation
  func (s Status) String() string {
  	switch s {
  	case StatusOk:
  		return "ok"
  	case StatusNg:
  		return "ng"
  	default:
  		panic(fmt.Sprintf("unexpected Status %v, in string()", s))
  	}
  
  }
  // ParseStatus : parse
  func ParseStatus(s string) Status {
  	switch s {
  	case "OK":
  		return StatusOk
  	case "NG":
  		return StatusNg
  	default:
  		panic(fmt.Sprintf("unexpected Status %v, in parse()", s))
  	}
  
  }
  
  // Greeter :
  type Greeter interface {
  	Greet() string
  }
  
  
  // MoreGreeter : hai
  type MoreGreeter interface {
  	Greeter
  	Greet2() string
  }
  
  
  // Person :
  type Person struct {
  	Name string // person's name
  	Age int
  	Father *Person
  	Mother *Person
  }
  
  
  // MorePerson :
  type MorePerson struct {
  	Person
  	memo string
  }

