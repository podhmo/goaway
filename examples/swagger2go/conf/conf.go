// Conf :
type Conf struct {
	Platforms Platforms `json:"platforms" bson:"platforms"`
	Description string `json:"description" bson:"description"`
	Accessories Accessories `json:"accessories" bson:"accessories"`
	Bridge *Bridge `json:"bridge" bson:"bridge"`
}

// Platforms :
type Platforms []PlatformsItem

// PlatformsItem :
type PlatformsItem struct {
	Platform string `json:"platform" bson:"platform"`
	Name string `json:"name" bson:"name"`
}

// Accessories :
type Accessories []AccessoriesItem

// AccessoriesItem :
type AccessoriesItem struct {
	Accessory string `json:"accessory" bson:"accessory"`
	Name string `json:"name" bson:"name"`
}

// Bridge :
type Bridge struct {
	Port int64 `json:"port" bson:"port"`
	Pin string `json:"pin" bson:"pin"`
	Username string `json:"username" bson:"username"`
	Name string `json:"name" bson:"name"`
}