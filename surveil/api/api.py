from pecanrest.controllers.api import order


class ApiController(object):
    orders = order.OrdersController()
