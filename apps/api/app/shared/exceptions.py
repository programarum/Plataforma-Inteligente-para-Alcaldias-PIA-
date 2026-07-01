"""Application-level exception types."""


class ApplicationError(Exception):
    """Base class for expected application errors."""


class NotFoundError(ApplicationError):
    """Raised when an application resource does not exist."""

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(detail)
