"""Motor driver implementation for Smart I2C Motor Driver."""

import logging
from typing import Optional

from ..transports import Transport, TransportError
from .protocol import (
    DEFAULT_ADDRESS,
    Direction,
    MotorID,
    MotorState,
    validate_address,
    validate_speed,
)

logger = logging.getLogger(__name__)


class MotorDriver:
    """Driver class for controlling a Smart I2C Motor.
    
    This class implements the Smart Driver Protocol to control a motor
    connected via I2C. The protocol uses a 4-step command sequence:
    1. T1: Motor ID (0x00 = Motor 0, 0x01 = Motor 1)
    2. T2: Activation (0x00 = DEACTIVATE, 0x01 = ACTIVATE)
    3. T3: Direction (0x00 = FORWARD, 0x01 = BACKWARD)
    4. T4: Speed (0x00-0xFF PWM value)
    
    Args:
        transport: Transport instance for I2C communication
        motor_id: Motor ID (MOTOR_0 or MOTOR_1)
        address: I2C address of the motor controller (default: 0x7F)
        
    Example:
        >>> from smi2c_master import I2CTransport, MotorDriver, MotorID
        >>> transport = I2CTransport(bus_number=1)
        >>> motor = MotorDriver(transport, MotorID.MOTOR_0)
        >>> motor.forward(128)  # Half speed forward
        >>> motor.stop()
        >>> transport.close()
        
    Example with context manager:
        >>> with I2CTransport() as transport:
        ...     motor = MotorDriver(transport, MotorID.MOTOR_1)
        ...     motor.backward(200)
        ...     motor.stop()
    """
    
    def __init__(self, transport: Transport, motor_id: MotorID, address: int = DEFAULT_ADDRESS):
        """Initialize the motor driver.
        
        Args:
            transport: Transport instance for communication
            motor_id: Motor ID (MOTOR_0 or MOTOR_1)
            address: I2C address of the motor controller
            
        Raises:
            InvalidAddressError: If address is out of valid range
            TypeError: If motor_id is not a MotorID enum value
        """
        validate_address(address)
        
        if not isinstance(motor_id, MotorID):
            raise TypeError(f"motor_id must be a MotorID enum value, got {type(motor_id).__name__}")
        
        self._transport = transport
        self._motor_id = motor_id
        self._address = address
        self._current_speed: Optional[int] = None
        self._is_active = False
        logger.info(f"Initialized motor driver for Motor {motor_id.value} at address 0x{address:02X}")
    
    def _send_motor_command(self, active: MotorState, direction: Direction, speed: int) -> None:
        """Send a complete 4-step command sequence to the I2C Slave.
        
        This function performs four separate I2C transactions (Start-Write-Stop cycles)
        matching the Arduino implementation.
        
        Args:
            active: Activation status (ACTIVATE or DEACTIVATE)
            direction: Direction (FORWARD or BACKWARD)
            speed: PWM speed value (0-255)
            
        Raises:
            TransportError: If any I2C transaction fails
        """
        validate_speed(speed)
        
        try:
            # T1: Send Motor ID (0x00 or 0x01)
            self._transport.write_byte(self._address, self._motor_id)
            logger.debug(f"T1 (Motor ID {self._motor_id.value}): OK")
            
            # T2: Send Activation Status (0x00 or 0x01)
            self._transport.write_byte(self._address, active)
            logger.debug(f"T2 (Active {active.value}): OK")
            
            # T3: Send Direction (0x00 or 0x01)
            self._transport.write_byte(self._address, direction)
            logger.debug(f"T3 (Direction {direction.value}): OK")
            
            # T4: Send Speed (0x00 to 0xFF)
            self._transport.write_byte(self._address, speed)
            logger.debug(f"T4 (Speed {speed}): OK")
            
            # Update internal state
            self._is_active = (active == MotorState.ACTIVATE)
            self._current_speed = speed
            
            logger.info(f"Command successfully sent to Motor {self._motor_id.value}")
            
        except TransportError as e:
            logger.error(f"Command FAILED for Motor {self._motor_id.value}: {e}")
            raise
    
    def forward(self, speed: int) -> None:
        """Run motor forward at specified speed.
        
        According to the new 4-step protocol:
        1. T1: Motor ID (0x00 = Motor 0, 0x01 = Motor 1)
        2. T2: Activate motor (0x01)
        3. T3: Set direction to forward (0x00)
        4. T4: Set speed (0x00-0xFF)
        
        Args:
            speed: Speed value (0-255, where 0=stopped, 255=full speed)
            
        Raises:
            InvalidSpeedError: If speed is out of valid range
            TransportError: If I2C communication fails
            
        Example:
            >>> motor.forward(200)  # Run forward at ~78% speed
        """
        self._send_motor_command(MotorState.ACTIVATE, Direction.FORWARD, speed)
        logger.info(f"Motor {self._motor_id.value}: forward at speed {speed}")
    
    def backward(self, speed: int) -> None:
        """Run motor backward at specified speed.
        
        According to the new 4-step protocol:
        1. T1: Motor ID (0x00 = Motor 0, 0x01 = Motor 1)
        2. T2: Activate motor (0x01)
        3. T3: Set direction to backward (0x01)
        4. T4: Set speed (0x00-0xFF)
        
        Args:
            speed: Speed value (0-255, where 0=stopped, 255=full speed)
            
        Raises:
            InvalidSpeedError: If speed is out of valid range
            TransportError: If I2C communication fails
            
        Example:
            >>> motor.backward(150)  # Run backward at ~59% speed
        """
        self._send_motor_command(MotorState.ACTIVATE, Direction.BACKWARD, speed)
        logger.info(f"Motor {self._motor_id.value}: backward at speed {speed}")
    
    def stop(self) -> None:
        """Stop the motor.
        
        According to the new 4-step protocol:
        1. T1: Motor ID (0x00 = Motor 0, 0x01 = Motor 1)
        2. T2: Deactivate motor (0x00)
        3. T3: Set direction (0x00 - value ignored when deactivated)
        4. T4: Set speed to 0 (0x00 - value ignored when deactivated)
        
        Note: When sending DEACTIVATE, the direction and speed bytes are technically ignored
        by the slave, but we must send all 4 bytes to complete the protocol.
        
        Raises:
            TransportError: If I2C communication fails
            
        Example:
            >>> motor.stop()
        """
        self._send_motor_command(MotorState.DEACTIVATE, Direction.FORWARD, 0)
        logger.info(f"Motor {self._motor_id.value}: stopped")
    
    @property
    def address(self) -> int:
        """Get the I2C address of this motor."""
        return self._address
    
    @property
    def motor_id(self) -> MotorID:
        """Get the motor ID."""
        return self._motor_id
    
    @property
    def current_speed(self) -> Optional[int]:
        """Get the last set speed value, or None if not set."""
        return self._current_speed
    
    @property
    def is_active(self) -> bool:
        """Check if the motor is currently active."""
        return self._is_active
