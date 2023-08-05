class AuthError(Exception):
    def __init__(self, error, status_code) -> None:
        self.error = error
        self.status_code = status_code