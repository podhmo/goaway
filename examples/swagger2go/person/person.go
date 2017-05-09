package person

import (
	"github/podhmo/another"
)

// People : 
type People []Person


// Person : 
type Person struct {
	Name string  `json:"name" bson:"name"`
	Age int64  `json:"age" bson:"age"`
	Gender Gender  `json:"gender" bson:"gender"`
	Memo Memo  `json:"memo" bson:"memo"`
	Memo2 another.Memo  `json:"memo2" bson:"memo2"`
	Father *Person  `json:"father" bson:"father"`
	Mother *Person  `json:"mother" bson:"mother"`
}