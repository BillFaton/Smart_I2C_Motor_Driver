"""Smart I2C Motor Driver - Python library for controlling I2C motor controllers.

This package provides a high-level interface for controlling motors via I2C
using the Smart Driver Protocol (4-step command sequence).

Basic Usage:
    >>> from smi2c_master import I2CTransport, MotorDriver, MotorID
    >>> 
    >>> # Create shared I2C transport
    >>> transport = I2CTransport(bus_number=1)
    >>> 
    >>> # Create motor driver instance for Motor 0
    >>> motor = MotorDriver(transport, MotorID.MOTOR_0)
    >>> 
    >>> # Control the motor
    >>> motor.forward(200)   # Run forward at speed 200
    >>> motor.backward(150)  # Run backward at speed 150
    >>> motor.stop()         # Stop the motor
    >>> 
    >>> # Clean up
    >>> transport.close()

With context manager:
    >>> with I2CTransport() as transport:
    ...     motor = MotorDriver(transport, MotorID.MOTOR_1)
    ...     motor.forward(128)
    ...     motor.stop()

Multiple motors on same slave:
    >>> transport = I2CTransport(bus_number=1)
    >>> motor0 = MotorDriver(transport, MotorID.MOTOR_0)  # Motor 0 on slave 0x7F
    >>> motor1 = MotorDriver(transport, MotorID.MOTOR_1)  # Motor 1 on slave 0x7F
    >>> motor0.forward(200)
    >>> motor1.backward(150)
"""

__version__ = "0.1.0"

from .core import (
    DEFAULT_ADDRESS,
    MAX_SPEED,
    MIN_SPEED,
    Direction,
    InvalidAddressError,
    InvalidSpeedError,
    MotorDriver,
    MotorID,
    MotorState,
    ProtocolError,
)
from .logging import get_logger, setup_logging
from .transports import I2CTransport, Transport, TransportError

__all__ = [
    # Version
    "__version__",
    # Core classes
    "MotorDriver",
    "Direction",
    "MotorID",
    "MotorState",
    # Transport classes
    "Transport",
    "I2CTransport",
    # Exceptions
    "ProtocolError",
    "InvalidSpeedError",
    "InvalidAddressError",
    "TransportError",
    # Constants
    "MIN_SPEED",
    "MAX_SPEED",
    "DEFAULT_ADDRESS",
    # Logging
    "setup_logging",
    "get_logger",
]
