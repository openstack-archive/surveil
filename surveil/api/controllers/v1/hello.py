import pecan
from pecan import rest


class HelloController(rest.RestController):

    @pecan.expose()
    def get(self):
        """Says hello."""
        return "Hello World!"
