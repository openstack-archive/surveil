test: clean start-mongo
	tox
	sudo docker stop surveil_test_mongo

integration: clean start-mongo
	tox -eintegration
	sudo docker stop surveil_test_mongo

clean:
	rm -rf pbr-*.egg
	rm -rf surveil.egg-info
	rm -rf .tox
	rm -rf .testrepository
	rm -rf doc/build
	- sudo docker kill surveil_test_mongo
	- sudo docker rm surveil_test_mongo

start-mongo:
	sudo docker pull mongo
	sudo docker run -d --name surveil_test_mongo -p 27017:27017 mongo mongod --smallfiles --noprealloc
