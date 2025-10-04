"""Tests for motor driver."""

from unittest.mock import Mock, call

import pytest

from smi2c_master import InvalidAddressError, MotorDriver
from smi2c_master.core.protocol import Direction, MotorState


class TestMotorDriverInit:
    """Test MotorDriver initialization."""
    
    def test_init_with_default_address(self):
        """Test initialization with default address."""
        transport = Mock()
        driver = MotorDriver(transport)
        assert driver.address == 0xFE
        assert driver.current_speed is None
        assert driver.is_active is False
    
    def test_init_with_custom_address(self):
        """Test initialization with custom address."""
        transport = Mock()
        driver = MotorDriver(transport, address=0x10)
        assert driver.address == 0x10
    
    def test_init_with_invalid_address(self):
        """Test initialization fails with invalid address."""
        transport = Mock()
        with pytest.raises(InvalidAddressError):
            MotorDriver(transport, address=0x80)


class TestMotorDriverForward:
    """Test forward motion."""
    
    def test_forward_sends_correct_sequence(self):
        """Test forward() sends correct I2C sequence."""
        transport = Mock()
        driver = MotorDriver(transport, address=0xFE)
        
        driver.forward(200)
        
        # Verify the sequence of calls
        assert transport.write_byte.call_count == 3
        calls = transport.write_byte.call_args_list
        assert calls[0] == call(0xFE, MotorState.ON)
        assert calls[1] == call(0xFE, Direction.FORWARD)
        assert calls[2] == call(0xFE, 200)
    
    def test_forward_updates_state(self):
        """Test forward() updates driver state."""
        transport = Mock()
        driver = MotorDriver(transport)
        
        driver.forward(150)
        
        assert driver.current_speed == 150
        assert driver.is_active is True
    
    def test_forward_zero_speed(self):
        """Test forward() with zero speed."""
        transport = Mock()
        driver = MotorDriver(transport)
        
        driver.forward(0)
        
        assert driver.current_speed == 0
        assert transport.write_byte.call_count == 3


class TestMotorDriverBackward:
    """Test backward motion."""
    
    def test_backward_sends_correct_sequence(self):
        """Test backward() sends correct I2C sequence."""
        transport = Mock()
        driver = MotorDriver(transport, address=0xFE)
        
        driver.backward(180)
        
        # Verify the sequence of calls
        assert transport.write_byte.call_count == 3
        calls = transport.write_byte.call_args_list
        assert calls[0] == call(0xFE, MotorState.ON)
        assert calls[1] == call(0xFE, Direction.BACKWARD)
        assert calls[2] == call(0xFE, 180)
    
    def test_backward_updates_state(self):
        """Test backward() updates driver state."""
        transport = Mock()
        driver = MotorDriver(transport)
        
        driver.backward(100)
        
        assert driver.current_speed == 100
        assert driver.is_active is True


class TestMotorDriverStop:
    """Test stop functionality."""
    
    def test_stop_sends_correct_sequence(self):
        """Test stop() sends correct I2C sequence."""
        transport = Mock()
        driver = MotorDriver(transport, address=0xFE)
        
        # First run motor, then stop
        driver.forward(200)
        transport.write_byte.reset_mock()
        
        driver.stop()
        
        # Verify the stop sequence
        assert transport.write_byte.call_count == 3
        calls = transport.write_byte.call_args_list
        assert calls[0] == call(0xFE, MotorState.OFF)
        assert calls[1] == call(0xFE, Direction.BACKWARD)
        assert calls[2] == call(0xFE, 0)
    
    def test_stop_updates_state(self):
        """Test stop() updates driver state."""
        transport = Mock()
        driver = MotorDriver(transport)
        
        driver.forward(200)
        driver.stop()
        
        assert driver.current_speed == 0
        assert driver.is_active is False


class TestMotorDriverProperties:
    """Test driver properties."""
    
    def test_address_property(self):
        """Test address property."""
        transport = Mock()
        driver = MotorDriver(transport, address=0x20)
        assert driver.address == 0x20
    
    def test_current_speed_property(self):
        """Test current_speed property."""
        transport = Mock()
        driver = MotorDriver(transport)
        
        assert driver.current_speed is None
        driver.forward(100)
        assert driver.current_speed == 100
    
    def test_is_active_property(self):
        """Test is_active property."""
        transport = Mock()
        driver = MotorDriver(transport)
        
        assert driver.is_active is False
        driver.forward(100)
        assert driver.is_active is True
        driver.stop()
        assert driver.is_active is False


class TestMotorDriverMultipleMotors:
    """Test multiple motor instances."""
    
    def test_multiple_motors_same_transport(self):
        """Test multiple motors can share the same transport."""
        transport = Mock()
        motor1 = MotorDriver(transport, address=0xFE)
        motor2 = MotorDriver(transport, address=0xFF)
        
        motor1.forward(200)
        motor2.backward(150)
        
        # Verify each motor gets its own commands
        calls = transport.write_byte.call_args_list
        
        # Motor 1 commands (first 3 calls)
        assert calls[0] == call(0xFE, MotorState.ON)
        assert calls[1] == call(0xFE, Direction.FORWARD)
        assert calls[2] == call(0xFE, 200)
        
        # Motor 2 commands (next 3 calls)
        assert calls[3] == call(0xFF, MotorState.ON)
        assert calls[4] == call(0xFF, Direction.BACKWARD)
        assert calls[5] == call(0xFF, 150)
