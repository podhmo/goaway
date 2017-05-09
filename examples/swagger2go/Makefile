default: conf person

conf:
	mkdir -p conf
	swagger2go conf.swagger.yaml --ref="#/definitions/conf" --position=. --package github/podhmo/swagger2go/conf --file conf.go

person:
	mkdir -p person
	swagger2go person.swagger.yaml --position=. --package  github/podhmo/swagger2go/person --file person.go

.PHONY: person conf
