"""Application-level exception definitions."""


class ApplicationError(Exception):
    """Base exception for expected application failures."""


class EntityNotFoundError(ApplicationError):
    """Report that a requested domain entity does not exist."""

    def __init__(self, entity_name: str, entity_id: object) -> None:
        """Initialize the error with a public entity name and identifier."""
        self.entity_name = entity_name
        self.entity_id = entity_id
        super().__init__(f"{entity_name} '{entity_id}' was not found")
