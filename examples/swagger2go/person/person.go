package person

// Person : 
type Person struct {
	Name string  `json:"name" bson:"name"`
	Age int64  `json:"age" bson:"age"`
	Father *Person  `json:"father" bson:"father"`
	Mother *Person  `json:"mother" bson:"mother"`
}