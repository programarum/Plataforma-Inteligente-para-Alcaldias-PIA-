"""Application-level exception types."""


class ApplicationError(Exception):
    """Base class for expected application errors."""


class NotFoundError(ApplicationError):
    """Raised when an application resource does not exist."""

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(detail)


class ConflictError(ApplicationError):
    """Raised when a unique or assignment invariant is violated."""

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(detail)


class AuthenticationError(ApplicationError):
    """Raised when supplied authentication cannot establish an identity."""

    def __init__(self, detail: str = "Could not validate credentials") -> None:
        self.detail = detail
        super().__init__(detail)


class AuthorizationError(ApplicationError):
    """Raised when an authenticated identity lacks an authorization grant."""

    def __init__(self, detail: str = "Insufficient permissions") -> None:
        self.detail = detail
        super().__init__(detail)
