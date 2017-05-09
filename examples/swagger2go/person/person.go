package person

import (
	"github/podhmo/another"
	"fmt"
)

// People : 
type People []Person


// Gender : 
type Gender string

const (
	// GenderNotKnown : 
	GenderNotKnown = Gender("notKnown")
	// GenderMale : 
	GenderMale = Gender("male")
	// GenderFemale : 
	GenderFemale = Gender("female")
	// GenderNotApplicable : 
	GenderNotApplicable = Gender("notApplicable")
)

// String : stringer implementation
func (g Gender) String() string {
	switch g {
	case GenderNotKnown:
		return "notKnown"
	case GenderMale:
		return "male"
	case GenderFemale:
		return "female"
	case GenderNotApplicable:
		return "notApplicable"
	default:
		panic(fmt.Sprintf("unexpected Gender %s, in string()", string(g)))
	}

}
// ParseGender : parse
func ParseGender(g string) Gender {
	switch g {
	case "notKnown":
		return GenderNotKnown
	case "male":
		return GenderMale
	case "female":
		return GenderFemale
	case "notApplicable":
		return GenderNotApplicable
	default:
		panic(fmt.Sprintf("unexpected Gender %v, in parse()", g))
	}

}

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