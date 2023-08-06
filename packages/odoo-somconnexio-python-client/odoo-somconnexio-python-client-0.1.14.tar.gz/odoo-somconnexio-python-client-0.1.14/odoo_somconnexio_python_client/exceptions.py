class HTTPError(Exception):
    message = "Network problem accessing Odoo API. Exception: \n {}"

    def __init__(self, error_msg):
        self.message = self.message.format(error_msg)
        super(HTTPError, self).__init__(self.message)


class BadRequestError(Exception):
    message = "BadRequest with the next body: \n {}"

    def __init__(self, body):
        self.message = self.message.format(body)
        super(HTTPError, self).__init__(self.message)


class ResourceNotFound(Exception):
    message = "ResourceNotFound. Resource: {} and filter: {}"

    def __init__(self, resource, filter):
        self.message = self.message.format(resource, filter)
        super(ResourceNotFound, self).__init__(self.message)
