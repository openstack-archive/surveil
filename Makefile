down:
	- sudo fig kill

up:
	sudo fig up &

test: clean
	tox

clean:
	rm -rf pbr-*.egg
	rm -rf surveil.egg-info
	rm -rf .tox
	rm -rf .testrepository
	rm -rf doc/build
