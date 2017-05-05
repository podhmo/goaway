package colors

import (
	"fmt"
)

// Color : colors
type Color string

const (
	// ColorRed : red color
	ColorRed = Color("red")
	// ColorBlue : blue color
	ColorBlue = Color("blue")
	// ColorYellow : yellow color
	ColorYellow = Color("yellow")
	// ColorGreen : green color
	ColorGreen = Color("green")
)

// String : stringer implementation
func (c Color) String() string {
	switch c {
	case ColorRed:
		return "red"
	case ColorBlue:
		return "blue"
	case ColorYellow:
		return "yellow"
	case ColorGreen:
		return "green"
	default:
		panic(fmt.Sprintf("unexpected Color %v, in string()", c))
	}

}
// ParseColor : parse
func ParseColor(c string) Color {
	switch c {
	case "red":
		return ColorRed
	case "blue":
		return ColorBlue
	case "yellow":
		return ColorYellow
	case "green":
		return ColorGreen
	default:
		panic(fmt.Sprintf("unexpected Color %v, in parse()", c))
	}

}