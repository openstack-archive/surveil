docker_build:
	sudo docker build -t surveil_image .

docker_rebuild:
	sudo docker build --no-cache=true -t surveil_image .

docker_kill:
	- sudo docker stop surveil
	- sudo docker rm surveil

docker_run: docker_kill docker_build
	sudo docker run -d -t --name surveil surveil_image
	sudo docker inspect --format='{{.NetworkSettings.IPAddress}}' surveil

docker_run_interactive: docker_kill docker_build
	sudo docker run -i -t --name surveil surveil_image bash

test: clean
	tox

clean:
	rm -rf pbr-*.egg
	rm -rf surveil.egg-info
	rm -rf .tox
	rm -rf .testrepository
	rm -rf doc/build
