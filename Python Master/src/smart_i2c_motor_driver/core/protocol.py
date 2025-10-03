"""Protocol definitions for the Smart I2C Motor Driver.

This module defines the communication protocol constants and validation
functions based on the Smart Driver Protocol specification.

Protocol Overview:
    The motor driver requires three sequential I2C write operations:
    1. Motor activation (0x00 = off, 0x01 = on)
    2. Direction (0x00 = forward, 0x01 = backward)
    3. Speed (0x00-0xFF PWM value)
"""

from enum import IntEnum
from typing import Final


class MotorState(IntEnum):
    """Motor activation states."""
    OFF = 0x00
    ON = 0x01


class Direction(IntEnum):
    """Motor direction values."""
    FORWARD = 0x00
    BACKWARD = 0x01


# Protocol constants
MIN_SPEED: Final[int] = 0
MAX_SPEED: Final[int] = 255
DEFAULT_ADDRESS: Final[int] = 0xFE


class ProtocolError(Exception):
    """Base exception for protocol-related errors."""
    pass


class InvalidSpeedError(ProtocolError):
    """Exception raised when speed value is out of valid range."""
    pass


class InvalidAddressError(ProtocolError):
    """Exception raised when I2C address is invalid."""
    pass


def validate_speed(speed: int) -> None:
    """Validate motor speed value.
    
    Args:
        speed: Speed value to validate (0-255)
        
    Raises:
        InvalidSpeedError: If speed is out of valid range
        TypeError: If speed is not an integer
    """
    if not isinstance(speed, int):
        raise TypeError(f"Speed must be an integer, got {type(speed).__name__}")
    
    if not MIN_SPEED <= speed <= MAX_SPEED:
        raise InvalidSpeedError(
            f"Speed must be between {MIN_SPEED} and {MAX_SPEED}, got {speed}"
        )


def validate_address(address: int) -> None:
    """Validate I2C address.
    
    Args:
        address: I2C address to validate (0x00-0x7F)
        
    Raises:
        InvalidAddressError: If address is out of valid range
        TypeError: If address is not an integer
    """
    if not isinstance(address, int):
        raise TypeError(f"Address must be an integer, got {type(address).__name__}")
    
    if not 0x00 <= address <= 0x7F:
        raise InvalidAddressError(
            f"I2C address must be 0x00-0x7F, got 0x{address:02X}"
        )
