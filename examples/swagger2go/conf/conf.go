package conf

// Accessories : 
type Accessories []AccessoriesItem


// Platforms : 
type Platforms []PlatformsItem


// Conf : 
type Conf struct {
	Bridge *Bridge  `json:"bridge" bson:"bridge"`
	Description string  `json:"description" bson:"description"`
	Accessories Accessories  `json:"accessories" bson:"accessories"`
	Platforms Platforms  `json:"platforms" bson:"platforms"`
}


// Bridge : 
type Bridge struct {
	Name string  `json:"name" bson:"name"`
	Username string  `json:"username" bson:"username"`
	Port int64  `json:"port" bson:"port"`
	Pin string  `json:"pin" bson:"pin"`
}


// AccessoriesItem : 
type AccessoriesItem struct {
	Accessory string  `json:"accessory" bson:"accessory"`
	Name string  `json:"name" bson:"name"`
}


// PlatformsItem : 
type PlatformsItem struct {
	Platform string  `json:"platform" bson:"platform"`
	Name string  `json:"name" bson:"name"`
}