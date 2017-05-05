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
