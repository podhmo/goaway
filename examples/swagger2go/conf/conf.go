// Conf :
type Conf struct {
	Platforms Platforms `json:"platforms" bson:"platforms"`
	Bridge *Bridge `json:"bridge" bson:"bridge"`
	Accessories Accessories `json:"accessories" bson:"accessories"`
	Description string `json:"description" bson:"description"`
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
	Username string `json:"username" bson:"username"`
	Name string `json:"name" bson:"name"`
	Pin string `json:"pin" bson:"pin"`
	Port int64 `json:"port" bson:"port"`
}

// Accessories :
type Accessories []AccessoriesItem

// AccessoriesItem :
type AccessoriesItem struct {
	Name string `json:"name" bson:"name"`
	Accessory string `json:"accessory" bson:"accessory"`
}
