# Core API Reference

This page documents the core motor driver functionality.

## MotorDriver

::: smart_i2c_motor_driver.core.driver.MotorDriver
    options:
      show_root_heading: true
      show_source: true

## Protocol

### Enums

::: smart_i2c_motor_driver.core.protocol.MotorState
    options:
      show_root_heading: true
      
::: smart_i2c_motor_driver.core.protocol.Direction
    options:
      show_root_heading: true

### Constants

::: smart_i2c_motor_driver.core.protocol
    options:
      show_root_heading: false
      members:
        - MIN_SPEED
        - MAX_SPEED
        - DEFAULT_ADDRESS

### Validation Functions

::: smart_i2c_motor_driver.core.protocol.validate_speed
    options:
      show_root_heading: true

::: smart_i2c_motor_driver.core.protocol.validate_address
    options:
      show_root_heading: true

### Exceptions

::: smart_i2c_motor_driver.core.protocol.ProtocolError
    options:
      show_root_heading: true

::: smart_i2c_motor_driver.core.protocol.InvalidSpeedError
    options:
      show_root_heading: true

::: smart_i2c_motor_driver.core.protocol.InvalidAddressError
    options:
      show_root_heading: true
