"""
Custom exceptions for Football League Manager API.

Contains application-specific exception classes for better
error handling and API responses.
"""

from fastapi import HTTPException, status


class FootballManagerException(Exception):
    """Base exception class for Football Manager application."""
    pass


class TeamNotFoundException(FootballManagerException):
    """Raised when a team is not found."""
    pass


class PlayerNotFoundException(FootballManagerException):
    """Raised when a player is not found."""
    pass


class MatchNotFoundException(FootballManagerException):
    """Raised when a match is not found."""
    pass


class UserNotFoundException(FootballManagerException):
    """Raised when a user is not found."""
    pass


class VenueNotFoundException(FootballManagerException):
    """Raised when a venue is not found."""
    pass


class CoachNotFoundException(FootballManagerException):
    """Raised when a coach is not found."""
    pass


class RefereeNotFoundException(FootballManagerException):
    """Raised when a referee is not found."""
    pass


class ValidationException(HTTPException):
    """Raised when business rule validation fails."""
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)


class DuplicateResourceException(HTTPException):
    """Raised when trying to create a resource that already exists."""
    def __init__(self, detail: str):
        super().__init__(status_code=409, detail=detail)


class InvalidDataException(FootballManagerException):
    """Raised when provided data is invalid."""
    pass


# HTTP Exception helpers
def not_found_exception(message: str) -> HTTPException:
    """Create a 404 HTTP exception."""
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=message
    )


def bad_request_exception(message: str) -> HTTPException:
    """Create a 400 HTTP exception."""
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=message
    )


def conflict_exception(message: str) -> HTTPException:
    """Create a 409 HTTP exception."""
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=message
    )
