
class ModuleError(Exception):
    def __init__(self, message):
        super().__init__(message)

class MissingManagerClass(ModuleError):
    def __init__(self, message):
        super().__init__(message)