# Core API Reference

This page documents the core motor driver functionality.

## MotorDriver

::: smi2c_master.core.driver.MotorDriver
    options:
      show_root_heading: true
      show_source: true

## Protocol

### Enums

::: smi2c_master.core.protocol.MotorState
    options:
      show_root_heading: true
      
::: smi2c_master.core.protocol.Direction
    options:
      show_root_heading: true

### Constants

::: smi2c_master.core.protocol
    options:
      show_root_heading: false
      members:
        - MIN_SPEED
        - MAX_SPEED
        - DEFAULT_ADDRESS

### Validation Functions

::: smi2c_master.core.protocol.validate_speed
    options:
      show_root_heading: true

::: smi2c_master.core.protocol.validate_address
    options:
      show_root_heading: true

### Exceptions

::: smi2c_master.core.protocol.ProtocolError
    options:
      show_root_heading: true

::: smi2c_master.core.protocol.InvalidSpeedError
    options:
      show_root_heading: true

::: smi2c_master.core.protocol.InvalidAddressError
    options:
      show_root_heading: true
