"""Core motor driver functionality."""

from .driver import MotorDriver
from .protocol import (
    DEFAULT_ADDRESS,
    MAX_SPEED,
    MIN_SPEED,
    Direction,
    InvalidAddressError,
    InvalidSpeedError,
    MotorState,
    ProtocolError,
)

__all__ = [
    "MotorDriver",
    "Direction",
    "MotorState",
    "ProtocolError",
    "InvalidSpeedError",
    "InvalidAddressError",
    "MIN_SPEED",
    "MAX_SPEED",
    "DEFAULT_ADDRESS",
]
