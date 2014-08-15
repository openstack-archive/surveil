build:
	sudo docker build -t surveil_image .

kill:
	- sudo docker stop surveil
	- sudo docker rm surveil

run: kill build
	sudo docker run -d -t --name surveil surveil_image
	sudo docker inspect --format='{{.NetworkSettings.IPAddress}}' surveil

run-interactive: kill build
	sudo docker run -i -t --name surveil surveil_image bash

test:
	tox

clean:
	rm -rf pbr-*.egg
	rm -rf surveil.egg-info
	rm -rf .tox
	rm -rf .testrepository
	rm -rf doc/build
