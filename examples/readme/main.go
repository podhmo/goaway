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
