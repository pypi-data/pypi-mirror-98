from dataclasses import dataclass


__all__ = [
    "MatchError",
]


@dataclass
class MatchError(Exception):
    """
    Exception for pattern matching errors (used internally, should NEVER happen).
    """

    message: None


@dataclass
class RuntimeFailure(Exception):
    """
    A failure of the Runtime system.
    """

    message: None
