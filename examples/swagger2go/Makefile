default:
	mkdir -p conf
	swagger2go swagger.yaml --ref="#/definitions/conf" --position=. --package conf --file conf.go

person:
	mkdir -p person
	swagger2go person.swagger.yaml --position=. --package person --file person.go
.PHONY: person
