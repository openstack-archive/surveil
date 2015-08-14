test: start-mongo
	tox

clean-test: clean stop-mongo start-mongo test

integration: clean stop-mongo start-mongo
	tox -eintegration
	stop-mongo

clean:
	rm -rf pbr-*.egg
	rm -rf surveil.egg-info
	rm -rf .tox
	rm -rf .testrepository
	rm -rf doc/build

start-mongo:
	sudo docker pull mongo
	- sudo docker run -d --name surveil_test_mongo -p 27017:27017 mongo mongod --smallfiles --noprealloc

make stop-mongo:
	- sudo docker stop surveil_test_mongo
	- sudo docker kill surveil_test_mongo
	- sudo docker rm surveil_test_mongo
