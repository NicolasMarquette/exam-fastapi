"""Security settings."""

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Key and algorithm for the security settings."""
    SECRET_KEY = "fe44733a1210ce665d86da0c3a9a38694f90529c7b60b72d1c45486b96737003"
    ALGORITHM = "HS256"


def get_settings():
    """Return the settings."""
    return Settings()

settings = Settings()