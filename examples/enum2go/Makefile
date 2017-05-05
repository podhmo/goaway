default:
	mkdir -p colors
	mkdir -p tiny
	enum2go --package colors --position=. enum.yaml
	enum2go --writer=./tiny.py:TinyWriter --package tiny --position=. enum.yaml
