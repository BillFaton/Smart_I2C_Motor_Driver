# Smart I2C Motor Driver

A Python library for controlling I2C motor controllers using the Smart Driver Protocol.

## Features

- 🚀 Simple and intuitive API
- 🔧 Support for multiple motors on the same I2C bus
- 🎯 Type hints for better IDE support
- ✅ Comprehensive test coverage
- 📚 Full documentation
- 🛠️ Command-line interface for quick testing
- 🔌 Extensible transport layer

## Quick Start

Install the package:

```bash
pip install smart-i2c-motor-driver
```

Basic usage:

```python
from smi2c_master import I2CTransport, MotorDriver

# Create I2C transport
transport = I2CTransport(bus_number=1)

# Create motor driver
motor = MotorDriver(transport, address=0xFE)

# Control the motor
motor.forward(200)   # Run forward at speed 200
motor.backward(150)  # Run backward at speed 150
motor.stop()         # Stop the motor

# Clean up
transport.close()
```

## Protocol

The Smart Driver Protocol requires three sequential I2C write operations:

1. **Motor activation** (0x00 = off, 0x01 = on)
2. **Direction** (0x00 = forward, 0x01 = backward)
3. **Speed** (0x00-0xFF PWM value)

The library handles this protocol automatically.

## Multiple Motors

Control multiple motors using the same I2C bus:

```python
from smi2c_master import I2CTransport, MotorDriver

# Shared transport
transport = I2CTransport(bus_number=1)

# Multiple motors with different addresses
motor1 = MotorDriver(transport, address=0xFE)
motor2 = MotorDriver(transport, address=0xFF)

# Control independently
motor1.forward(200)
motor2.backward(150)
```

## Command-Line Interface

Test motors quickly from the command line:

```bash
# Run motor forward
smart-motor forward 200

# Run motor backward with duration
smart-motor backward 150 --duration 2.0

# Stop motor
smart-motor stop

# Use custom address and bus
smart-motor --bus 1 --address 0xFF forward 128
```

## Next Steps

- [Installation Guide](installation.md) - Detailed installation instructions
- [Getting Started](getting-started.md) - Step-by-step tutorial
- [User Guide](user-guide/basic-usage.md) - Learn all the features
- [API Reference](reference/core.md) - Complete API documentation
