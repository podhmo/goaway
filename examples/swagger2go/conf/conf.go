package conf

// Accessories : 
type Accessories []AccessoriesItem


// Platforms : 
type Platforms []PlatformsItem


// Conf : 
type Conf struct {
	Bridge *Bridge `json:"bridge"`
	Description string `json:"description"`
	Accessories Accessories `json:"accessories"`
	Platforms Platforms `json:"platforms"`
}


// Bridge : 
type Bridge struct {
	Name string `json:"name"`
	Username string `json:"username"`
	Port int64 `json:"port"`
	Pin string `json:"pin"`
}


// AccessoriesItem : 
type AccessoriesItem struct {
	Accessory string `json:"accessory"`
	Name string `json:"name"`
}


// PlatformsItem : 
type PlatformsItem struct {
	Platform string `json:"platform"`
	Name string `json:"name"`
}