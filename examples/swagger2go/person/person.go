package person

import (
	"github/podhmo/another"
)

// People : 
type People []Person


// People2 : 
type People2 []Person2


// Person : 
type Person struct {
	Name string  `json:"name" bson:"name"`
	Age int64  `json:"age" bson:"age"`
	Memo Memo  `json:"memo" bson:"memo"`
	Memo2 another.Memo  `json:"memo2" bson:"memo2"`
	Father *Person  `json:"father" bson:"father"`
	Mother *Person  `json:"mother" bson:"mother"`
}


// Person2 : 
type Person2 struct {
	Name string  `json:"name" bson:"name"`
	Age int64  `json:"age" bson:"age"`
	Memo Memo  `json:"memo" bson:"memo"`
	Memo2 another.Memo  `json:"memo2" bson:"memo2"`
	Father *Person2  `json:"father" bson:"father"`
	Mother *Person2  `json:"mother" bson:"mother"`
}