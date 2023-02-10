class HttpError(Exception):

    def __init__(self):
        self._code = 500
        self._name = 'Unknown error'
        self.description = 'Was not able to found exception handler for specified error'

    def get_response(self, message, sub_route=None):
        return {
            'code': self._code,
            'name': self._name,
            'description': self.description,
            'exc-message': message
        }
        
    @staticmethod
    def default_response(message, sub_route=None):
        return { 'exc-message': message }

class NotFound404Error(HttpError):
    def __init__(self, message):
        super().__init__(message)