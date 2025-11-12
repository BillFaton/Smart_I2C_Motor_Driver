"""Core motor driver functionality."""

from .driver import MotorDriver
from .protocol import (
    DEFAULT_ADDRESS,
    MAX_SPEED,
    MIN_SPEED,
    Direction,
    InvalidAddressError,
    InvalidSpeedError,
    MotorID,
    MotorState,
    ProtocolError,
)

__all__ = [
    "MotorDriver",
    "Direction",
    "MotorID",
    "MotorState",
    "ProtocolError",
    "InvalidSpeedError",
    "InvalidAddressError",
    "MIN_SPEED",
    "MAX_SPEED",
    "DEFAULT_ADDRESS",
]
