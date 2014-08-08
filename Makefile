build:
	sudo docker build -t surveil_image tools/test_env

kill:
	- sudo docker stop surveil
	- sudo docker rm surveil

run: kill build
	sudo docker run -d -t --name surveil surveil_image
	sudo docker inspect --format='{{.NetworkSettings.IPAddress}}' surveil

run-interactive: kill build
	sudo docker run -i -t --name surveil surveil_image bash
