"""Custom exceptions."""

class InhibitionBargraphException(Exception):
    """Basic exception for this application."""

class DatasetNotFound(InhibitionBargraphException):
    """Raised when a dataset url specified by the user cannot be found."""
