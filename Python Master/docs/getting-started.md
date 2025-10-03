# Getting Started

This guide will walk you through your first steps with the Smart I2C Motor Driver library.

## Prerequisites

Before starting, ensure you have:

- Completed the [installation](installation.md)
- I2C-enabled hardware (e.g., Raspberry Pi)
- A motor controller using the Smart Driver Protocol
- Motor controller connected to I2C bus

## Your First Motor Control

### Step 1: Import the Library

```python
from smart_i2c_motor_driver import I2CTransport, MotorDriver
```

### Step 2: Create a Transport

The transport manages the I2C bus connection:

```python
# Use I2C bus 1 (default for Raspberry Pi)
transport = I2CTransport(bus_number=1)
```

### Step 3: Create a Motor Driver

```python
# Connect to motor at address 0xFE (default)
motor = MotorDriver(transport, address=0xFE)
```

### Step 4: Control the Motor

```python
# Run forward at speed 200 (0-255 range)
motor.forward(200)

# Wait a bit
import time
time.sleep(2)

# Run backward at speed 150
motor.backward(150)
time.sleep(2)

# Stop the motor
motor.stop()
```

### Step 5: Clean Up

Always close the transport when done:

```python
transport.close()
```

## Complete Example

Here's a complete working example:

```python
import time
from smart_i2c_motor_driver import I2CTransport, MotorDriver

def main():
    # Create transport
    transport = I2CTransport(bus_number=1)
    
    try:
        # Create motor driver
        motor = MotorDriver(transport, address=0xFE)
        
        # Forward for 2 seconds
        print("Moving forward...")
        motor.forward(200)
        time.sleep(2)
        
        # Backward for 2 seconds
        print("Moving backward...")
        motor.backward(150)
        time.sleep(2)
        
        # Stop
        print("Stopping...")
        motor.stop()
        
    finally:
        # Always clean up
        transport.close()

if __name__ == "__main__":
    main()
```

## Using Context Managers

For automatic cleanup, use context managers:

```python
import time
from smart_i2c_motor_driver import I2CTransport, MotorDriver

with I2CTransport(bus_number=1) as transport:
    motor = MotorDriver(transport, address=0xFE)
    
    motor.forward(200)
    time.sleep(2)
    
    motor.stop()
    
# Transport automatically closed here
```

## Multiple Motors

Control multiple motors on the same bus:

```python
from smart_i2c_motor_driver import I2CTransport, MotorDriver

with I2CTransport(bus_number=1) as transport:
    # Create multiple motor instances
    left_motor = MotorDriver(transport, address=0xFE)
    right_motor = MotorDriver(transport, address=0xFF)
    
    # Control them independently
    left_motor.forward(200)
    right_motor.forward(180)  # Slightly slower
    
    time.sleep(2)
    
    # Stop both
    left_motor.stop()
    right_motor.stop()
```

## Error Handling

Always handle potential errors:

```python
from smart_i2c_motor_driver import (
    I2CTransport,
    MotorDriver,
    InvalidSpeedError,
    TransportError,
)

try:
    with I2CTransport(bus_number=1) as transport:
        motor = MotorDriver(transport)
        motor.forward(200)
        
except InvalidSpeedError as e:
    print(f"Invalid speed value: {e}")
except TransportError as e:
    print(f"I2C communication error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Logging

Enable logging to debug issues:

```python
import logging
from smart_i2c_motor_driver import setup_logging

# Enable debug logging
setup_logging(level=logging.DEBUG)

# Now all I2C operations will be logged
```

## Next Steps

- Learn about [Basic Usage](user-guide/basic-usage.md)
- Explore the [CLI](user-guide/cli.md)
- Check the [API Reference](reference/core.md)
- Read [Troubleshooting](troubleshooting.md) if you encounter issues
