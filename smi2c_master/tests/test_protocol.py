"""Tests for protocol module."""

import pytest

from smi2c_master.core.protocol import (
    DEFAULT_ADDRESS,
    MAX_SPEED,
    MIN_SPEED,
    Direction,
    InvalidAddressError,
    InvalidSpeedError,
    MotorState,
    validate_address,
    validate_speed,
)


class TestEnums:
    """Test protocol enums."""
    
    def test_motor_state_values(self):
        """Test MotorState enum values."""
        assert MotorState.OFF == 0x00
        assert MotorState.ON == 0x01
    
    def test_direction_values(self):
        """Test Direction enum values."""
        assert Direction.FORWARD == 0x00
        assert Direction.BACKWARD == 0x01


class TestConstants:
    """Test protocol constants."""
    
    def test_speed_range(self):
        """Test speed range constants."""
        assert MIN_SPEED == 0
        assert MAX_SPEED == 255
    
    def test_default_address(self):
        """Test default I2C address."""
        assert DEFAULT_ADDRESS == 0xFE


class TestValidateSpeed:
    """Test speed validation function."""
    
    def test_valid_speeds(self):
        """Test validation passes for valid speeds."""
        validate_speed(0)
        validate_speed(128)
        validate_speed(255)
    
    def test_invalid_speed_below_min(self):
        """Test validation fails for speed below minimum."""
        with pytest.raises(InvalidSpeedError, match="must be between"):
            validate_speed(-1)
    
    def test_invalid_speed_above_max(self):
        """Test validation fails for speed above maximum."""
        with pytest.raises(InvalidSpeedError, match="must be between"):
            validate_speed(256)
    
    def test_invalid_speed_type(self):
        """Test validation fails for non-integer speed."""
        with pytest.raises(TypeError, match="must be an integer"):
            validate_speed("100")
        
        with pytest.raises(TypeError, match="must be an integer"):
            validate_speed(100.5)


class TestValidateAddress:
    """Test address validation function."""
    
    def test_valid_addresses(self):
        """Test validation passes for valid addresses."""
        validate_address(0x00)
        validate_address(0x3F)
        validate_address(0x7F)
    
    def test_invalid_address_below_min(self):
        """Test validation fails for address below minimum."""
        with pytest.raises(InvalidAddressError, match="must be 0x00-0x7F"):
            validate_address(-1)
    
    def test_invalid_address_above_max(self):
        """Test validation fails for address above maximum."""
        with pytest.raises(InvalidAddressError, match="must be 0x00-0x7F"):
            validate_address(0x80)
    
    def test_invalid_address_type(self):
        """Test validation fails for non-integer address."""
        with pytest.raises(TypeError, match="must be an integer"):
            validate_address("0xFE")
        
        with pytest.raises(TypeError, match="must be an integer"):
            validate_address(0xFE + 0.1)
