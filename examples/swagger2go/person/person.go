package person

// People :
type People []Person

// People2 :
type People2 []Person2

// Memo :
type Memo struct {
	Name string `json:"name" bson:"name"`
}

// Person :
type Person struct {
	Name   string  `json:"name" bson:"name"`
	Age    int64   `json:"age" bson:"age"`
	Memo   Memo    `json:"memo" bson:"memo"`
	Father *Person `json:"father" bson:"father"`
	Mother *Person `json:"mother" bson:"mother"`
}

// Person2 :
type Person2 struct {
	Name   string   `json:"name" bson:"name"`
	Age    int64    `json:"age" bson:"age"`
	Memo   Memo     `json:"memo" bson:"memo"`
	Father *Person2 `json:"father" bson:"father"`
	Mother *Person2 `json:"mother" bson:"mother"`
}
