down:
	- sudo fig kill

up:
	sudo fig up &

build:
	sudo fig build

test: clean
	tox

clean:
	rm -rf pbr-*.egg
	rm -rf surveil.egg-info
	rm -rf .tox
	rm -rf .testrepository
	rm -rf doc/build
