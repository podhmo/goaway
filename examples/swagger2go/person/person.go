package person

import (
	"github/podhmo/another"
)

// People : 
type People []Person


// Person : 
type Person struct {
	Name string `json:"name"`
	Age int64 `json:"age"`
	Gender Gender `json:"gender"`
	Memo Memo `json:"memo"`
	Memo2 another.Memo `json:"memo2"`
	Father *Person `json:"father"`
	Mother *Person `json:"mother"`
}