"""Motor driver implementation for Smart I2C Motor Driver."""

import logging
from typing import Optional

from ..transports import Transport
from .protocol import (
    DEFAULT_ADDRESS,
    Direction,
    MotorState,
    validate_address,
    validate_speed,
)

logger = logging.getLogger(__name__)


class MotorDriver:
    """Driver class for controlling a Smart I2C Motor.
    
    This class implements the Smart Driver Protocol to control a motor
    connected via I2C. Multiple motor instances can share the same transport
    (I2C bus) while using different addresses.
    
    Args:
        transport: Transport instance for I2C communication
        address: I2C address of the motor controller (default: 0xFE)
        
    Example:
        >>> from smart_i2c_motor_driver import I2CTransport, MotorDriver
        >>> transport = I2CTransport(bus_number=1)
        >>> motor = MotorDriver(transport, address=0xFE)
        >>> motor.forward(128)  # Half speed forward
        >>> motor.stop()
        >>> transport.close()
        
    Example with context manager:
        >>> with I2CTransport() as transport:
        ...     motor = MotorDriver(transport)
        ...     motor.backward(200)
        ...     motor.stop()
    """
    
    def __init__(self, transport: Transport, address: int = DEFAULT_ADDRESS):
        """Initialize the motor driver.
        
        Args:
            transport: Transport instance for communication
            address: I2C address of the motor controller
            
        Raises:
            InvalidAddressError: If address is out of valid range
        """
        validate_address(address)
        self._transport = transport
        self._address = address
        self._current_speed: Optional[int] = None
        self._is_active = False
        logger.info(f"Initialized motor driver at address 0x{address:02X}")
    
    def _write_byte(self, data: int) -> None:
        """Write a byte to the motor controller.
        
        Args:
            data: Byte to write
        """
        self._transport.write_byte(self._address, data)
    
    def _set_state(self, state: MotorState) -> None:
        """Set motor activation state.
        
        Args:
            state: Motor state (ON or OFF)
        """
        self._write_byte(state)
        self._is_active = (state == MotorState.ON)
        logger.debug(f"Motor 0x{self._address:02X}: state={state.name}")
    
    def _set_direction(self, direction: Direction) -> None:
        """Set motor direction.
        
        Args:
            direction: Direction (FORWARD or BACKWARD)
        """
        self._write_byte(direction)
        logger.debug(f"Motor 0x{self._address:02X}: direction={direction.name}")
    
    def _set_speed(self, speed: int) -> None:
        """Set motor speed.
        
        Args:
            speed: Speed value (0-255)
        """
        validate_speed(speed)
        self._write_byte(speed)
        self._current_speed = speed
        logger.debug(f"Motor 0x{self._address:02X}: speed={speed}")
    
    def forward(self, speed: int) -> None:
        """Run motor forward at specified speed.
        
        According to the protocol:
        1. Activate motor (0x01)
        2. Set direction to forward (0x00)
        3. Set speed (0x00-0xFF)
        
        Args:
            speed: Speed value (0-255, where 0=stopped, 255=full speed)
            
        Raises:
            InvalidSpeedError: If speed is out of valid range
            TransportError: If I2C communication fails
            
        Example:
            >>> motor.forward(200)  # Run forward at ~78% speed
        """
        validate_speed(speed)
        self._set_state(MotorState.ON)
        self._set_direction(Direction.FORWARD)
        self._set_speed(speed)
        logger.info(f"Motor 0x{self._address:02X}: forward at speed {speed}")
    
    def backward(self, speed: int) -> None:
        """Run motor backward at specified speed.
        
        According to the protocol:
        1. Activate motor (0x01)
        2. Set direction to backward (0x01)
        3. Set speed (0x00-0xFF)
        
        Args:
            speed: Speed value (0-255, where 0=stopped, 255=full speed)
            
        Raises:
            InvalidSpeedError: If speed is out of valid range
            TransportError: If I2C communication fails
            
        Example:
            >>> motor.backward(150)  # Run backward at ~59% speed
        """
        validate_speed(speed)
        self._set_state(MotorState.ON)
        self._set_direction(Direction.BACKWARD)
        self._set_speed(speed)
        logger.info(f"Motor 0x{self._address:02X}: backward at speed {speed}")
    
    def stop(self) -> None:
        """Stop the motor.
        
        According to the protocol:
        1. Deactivate motor (0x00)
        2. Set direction to backward (0x01)
        3. Set speed to 0 (0x00)
        
        Raises:
            TransportError: If I2C communication fails
            
        Example:
            >>> motor.stop()
        """
        self._set_state(MotorState.OFF)
        self._set_direction(Direction.BACKWARD)
        self._set_speed(0)
        logger.info(f"Motor 0x{self._address:02X}: stopped")
    
    @property
    def address(self) -> int:
        """Get the I2C address of this motor."""
        return self._address
    
    @property
    def current_speed(self) -> Optional[int]:
        """Get the last set speed value, or None if not set."""
        return self._current_speed
    
    @property
    def is_active(self) -> bool:
        """Check if the motor is currently active."""
        return self._is_active
