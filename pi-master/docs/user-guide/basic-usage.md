# Basic Usage

This guide covers the common usage patterns for the Smart I2C Motor Driver library.

## Creating a Transport

The transport manages the I2C bus connection. All motor drivers share a single transport instance:

```python
from smi2c_master import I2CTransport

# Default bus (1)
transport = I2CTransport()

# Custom bus
transport = I2CTransport(bus_number=0)
```

## Creating Motor Drivers

Create motor driver instances for each motor:

```python
from smi2c_master import MotorDriver

# Default address (0xFE)
motor = MotorDriver(transport)

# Custom address
motor = MotorDriver(transport, address=0x10)
```

## Motor Control

### Forward Motion

```python
# Run forward at full speed
motor.forward(255)

# Run forward at half speed
motor.forward(128)

# Run forward slowly
motor.forward(50)
```

### Backward Motion

```python
# Run backward at full speed
motor.backward(255)

# Run backward at half speed
motor.backward(128)
```

### Stopping

```python
# Stop the motor
motor.stop()
```

## Speed Control

Speed values range from 0 to 255:

- `0` - Motor stopped
- `1-127` - Low to medium speeds
- `128-254` - Medium to high speeds
- `255` - Full speed

```python
# Different speed examples
motor.forward(64)   # 25% speed
motor.forward(128)  # 50% speed
motor.forward(192)  # 75% speed
motor.forward(255)  # 100% speed
```

## Multiple Motors

Control multiple motors independently:

```python
from smi2c_master import I2CTransport, MotorDriver

# Shared transport
transport = I2CTransport(bus_number=1)

# Create multiple motors
left_motor = MotorDriver(transport, address=0xFE)
right_motor = MotorDriver(transport, address=0xFF)

# Control independently
left_motor.forward(200)
right_motor.forward(180)

# Stop both
left_motor.stop()
right_motor.stop()

# Cleanup
transport.close()
```

## Motor Properties

Access motor state information:

```python
motor = MotorDriver(transport)

# Get the I2C address
print(motor.address)  # 0xFE

# Check if motor is active
print(motor.is_active)  # False initially

motor.forward(200)
print(motor.is_active)  # True after starting

# Get current speed
print(motor.current_speed)  # 200

motor.stop()
print(motor.is_active)  # False after stopping
```

## Context Managers

Use context managers for automatic cleanup:

```python
from smi2c_master import I2CTransport, MotorDriver

# Transport context manager
with I2CTransport(bus_number=1) as transport:
    motor = MotorDriver(transport)
    motor.forward(200)
    motor.stop()
# Transport automatically closed
```

## Error Handling

Handle common errors:

```python
from smi2c_master import (
    I2CTransport,
    MotorDriver,
    InvalidSpeedError,
    InvalidAddressError,
    TransportError,
)

try:
    transport = I2CTransport(bus_number=1)
    motor = MotorDriver(transport, address=0xFE)
    motor.forward(200)
    
except InvalidSpeedError as e:
    print(f"Invalid speed: {e}")
    
except InvalidAddressError as e:
    print(f"Invalid address: {e}")
    
except TransportError as e:
    print(f"I2C error: {e}")
    
finally:
    transport.close()
```

## Timing and Delays

Control motor timing with delays:

```python
import time
from smi2c_master import I2CTransport, MotorDriver

with I2CTransport() as transport:
    motor = MotorDriver(transport)
    
    # Forward for 3 seconds
    motor.forward(200)
    time.sleep(3)
    
    # Backward for 2 seconds
    motor.backward(150)
    time.sleep(2)
    
    # Stop
    motor.stop()
```

## Robot Movement Patterns

### Straight Line

```python
def move_straight(left_motor, right_motor, speed, duration):
    """Move robot straight forward."""
    left_motor.forward(speed)
    right_motor.forward(speed)
    time.sleep(duration)
    left_motor.stop()
    right_motor.stop()
```

### Turn in Place

```python
def turn_right(left_motor, right_motor, speed, duration):
    """Turn robot right in place."""
    left_motor.forward(speed)
    right_motor.backward(speed)
    time.sleep(duration)
    left_motor.stop()
    right_motor.stop()

def turn_left(left_motor, right_motor, speed, duration):
    """Turn robot left in place."""
    left_motor.backward(speed)
    right_motor.forward(speed)
    time.sleep(duration)
    left_motor.stop()
    right_motor.stop()
```

### Gradual Turn

```python
def gradual_turn_right(left_motor, right_motor, duration):
    """Gradual right turn."""
    left_motor.forward(200)
    right_motor.forward(100)  # Slower
    time.sleep(duration)
    left_motor.stop()
    right_motor.stop()
```

## Logging

Enable logging for debugging:

```python
import logging
from smi2c_master import setup_logging

# Info level (default)
setup_logging(level=logging.INFO)

# Debug level (verbose)
setup_logging(level=logging.DEBUG)

# Custom format
setup_logging(
    level=logging.DEBUG,
    format_string="%(levelname)s: %(message)s"
)
```

## Best Practices

1. **Always clean up**: Use context managers or call `transport.close()`
2. **Share transports**: Use one transport for multiple motors
3. **Handle errors**: Wrap I2C operations in try/except blocks
4. **Validate inputs**: The library validates speed and address values
5. **Stop before exit**: Always stop motors before program termination

## Complete Example

```python
import time
import logging
from smi2c_master import (
    I2CTransport,
    MotorDriver,
    setup_logging,
    TransportError,
)

def main():
    # Enable logging
    setup_logging(level=logging.INFO)
    
    try:
        # Create transport
        with I2CTransport(bus_number=1) as transport:
            # Create motors
            left = MotorDriver(transport, address=0xFE)
            right = MotorDriver(transport, address=0xFF)
            
            # Move forward
            print("Forward...")
            left.forward(200)
            right.forward(200)
            time.sleep(2)
            
            # Turn right
            print("Turn right...")
            left.forward(200)
            right.backward(200)
            time.sleep(1)
            
            # Backward
            print("Backward...")
            left.backward(150)
            right.backward(150)
            time.sleep(2)
            
            # Stop
            print("Stop")
            left.stop()
            right.stop()
            
    except TransportError as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nStopped by user")

if __name__ == "__main__":
    main()
```

## Next Steps

- [CLI Usage](cli.md) - Use the command-line interface
- [API Reference](../reference/core.md) - Complete API documentation
- [Troubleshooting](../troubleshooting.md) - Common issues and solutions
