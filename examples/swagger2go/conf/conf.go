// Conf :
type Conf struct {
	Accessories Accessories `json:"accessories" bson:"accessories"`
	Platforms Platforms `json:"platforms" bson:"platforms"`
	Bridge *Bridge `json:"bridge" bson:"bridge"`
	Description string `json:"description" bson:"description"`
}

// Accessories :
type Accessories []AccessoriesItem

// AccessoriesItem :
type AccessoriesItem struct {
	Name string `json:"name" bson:"name"`
	Accessory string `json:"accessory" bson:"accessory"`
}

// Platforms :
type Platforms []PlatformsItem

// PlatformsItem :
type PlatformsItem struct {
	Name string `json:"name" bson:"name"`
	Platform string `json:"platform" bson:"platform"`
}

// Bridge :
type Bridge struct {
	Name string `json:"name" bson:"name"`
	Username string `json:"username" bson:"username"`
	Pin string `json:"pin" bson:"pin"`
	Port int64 `json:"port" bson:"port"`
}
