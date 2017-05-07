package colors

import (
	"fmt"
)

// Priority : 
type Priority int

const (
	// PriorityHigh : 
	PriorityHigh = Priority(1)
	// PriorityNormal : 
	PriorityNormal = Priority(0)
	// PriorityLow : 
	PriorityLow = Priority(-1)
)

// String : stringer implementation
func (p Priority) String() string {
	switch p {
	case PriorityHigh:
		return "high"
	case PriorityNormal:
		return "normal"
	case PriorityLow:
		return "low"
	default:
		panic(fmt.Sprintf("unexpected Priority %v, in string()", p))
	}

}
// ParsePriority : parse
func ParsePriority(p int) Priority {
	switch p {
	case 1:
		return PriorityHigh
	case 0:
		return PriorityNormal
	case -1:
		return PriorityLow
	default:
		panic(fmt.Sprintf("unexpected Priority %v, in parse()", p))
	}

}