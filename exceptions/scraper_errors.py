
class ScraperLoadingError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class MissingScraperClass(ScraperLoadingError):
    def __init__(self, message):
        super().__init__(message)

