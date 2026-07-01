"""Application logging configuration."""

import logging


def configure_logging(log_level: str) -> None:
    """Configure process logging using the requested severity level."""
    level = getattr(logging, log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
