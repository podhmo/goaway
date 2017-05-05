default:
	python main.py > main.go
	goimports -w main.go
	go run main.go

setup:
	go get -v golang.org/x/tools/cmd/goimports
