import pecan
from pecan import rest


class HelloController(rest.RestController):

    @pecan.expose()
    def get(self):
        return "Hello World!"
