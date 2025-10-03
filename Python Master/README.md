# Smart I2C Motor Driver

A Python library for controlling I2C motor controllers using the Smart Driver Protocol.

[![Documentation](https://img.shields.io/badge/docs-mkdocs-blue)](https://yourusername.github.io/smart-i2c-motor-driver)
[![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Features

- 🚀 **Simple API** - Easy to use, intuitive interface
- 🔧 **Multiple Motors** - Control multiple motors on the same I2C bus
- 🎯 **Type Hints** - Full type annotations for better IDE support
- ✅ **Well Tested** - Comprehensive test coverage
- 📚 **Documented** - Complete documentation with examples
- 🛠️ **CLI Tool** - Command-line interface for quick testing
- 🔌 **Extensible** - Pluggable transport layer architecture

## Quick Start

⚡ **New to the project?** Check out [QUICKSTART_UV.md](QUICKSTART_UV.md) for a fast setup guide using uv!

### Installation

Using pip:
```bash
pip install smart-i2c-motor-driver
```

Using uv (recommended - 10-100x faster):
```bash
uv pip install smart-i2c-motor-driver
```

### Basic Usage

```python
from smart_i2c_motor_driver import I2CTransport, MotorDriver

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

### With Context Manager

```python
from smart_i2c_motor_driver import I2CTransport, MotorDriver

with I2CTransport() as transport:
    motor = MotorDriver(transport)
    motor.forward(128)
    motor.stop()
```

### Command-Line Interface

```bash
# Install with CLI support
pip install smart-i2c-motor-driver[cli]

# Run motor forward
smart-motor forward 200

# Run motor backward for 2 seconds
smart-motor backward 150 --duration 2.0

# Stop motor
smart-motor stop
```

## Protocol

The Smart Driver Protocol requires three sequential I2C write operations:

1. **Motor activation** (0x00 = off, 0x01 = on)
2. **Direction** (0x00 = forward, 0x01 = backward)
3. **Speed** (0x00-0xFF PWM value)

This library handles the protocol automatically.

## Documentation

Full documentation is available at: [https://yourusername.github.io/smart-i2c-motor-driver](https://yourusername.github.io/smart-i2c-motor-driver)

- [Installation Guide](https://yourusername.github.io/smart-i2c-motor-driver/installation)
- [Getting Started](https://yourusername.github.io/smart-i2c-motor-driver/getting-started)
- [User Guide](https://yourusername.github.io/smart-i2c-motor-driver/user-guide/basic-usage)
- [API Reference](https://yourusername.github.io/smart-i2c-motor-driver/reference/core)
- [Troubleshooting](https://yourusername.github.io/smart-i2c-motor-driver/troubleshooting)

## Requirements

- Python 3.13 or higher
- I2C-enabled hardware (e.g., Raspberry Pi)
- smbus2 library

## Development

### Setup Development Environment

Using pip:
```bash
git clone https://github.com/yourusername/smart-i2c-motor-driver.git
cd smart-i2c-motor-driver/Python\ Master
pip install -e .[dev]
```

Using uv (faster):
```bash
git clone https://github.com/yourusername/smart-i2c-motor-driver.git
cd smart-i2c-motor-driver/Python\ Master
uv venv
source .venv/bin/activate  # On macOS/Linux
uv pip install -e '.[dev]'
```

### Run Tests

```bash
pytest
```

### Run Tests with Coverage

```bash
pytest --cov=smart_i2c_motor_driver --cov-report=html
```

### Build Documentation Locally

```bash
mkdocs serve
```

Then visit http://127.0.0.1:8000

### GitHub Pages

Documentation is automatically deployed to GitHub Pages when pushing to the main branch. Visit:
https://yourusername.github.io/smart-i2c-motor-driver

## Project Structure

```
Python Master/
├── src/
│   └── smart_i2c_motor_driver/
│       ├── __init__.py
│       ├── logging.py
│       ├── core/
│       │   ├── driver.py
│       │   └── protocol.py
│       └── transports/
│           ├── base.py
│           └── i2c.py
├── app/
│   └── cli.py
├── tests/
│   ├── test_driver.py
│   └── test_protocol.py
├── docs/
│   └── ...
├── pyproject.toml
└── mkdocs.yml
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## Acknowledgments

- Smart Driver Protocol specification by [your colleague's name]
- Built for ATtiny-based I2C motor controllers

## Support

- 📖 [Documentation](https://yourusername.github.io/smart-i2c-motor-driver)
- 🐛 [Issue Tracker](https://github.com/yourusername/smart-i2c-motor-driver/issues)
- 💬 [Discussions](https://github.com/yourusername/smart-i2c-motor-driver/discussions)

## Examples

### Multiple Motors

```python
from smart_i2c_motor_driver import I2CTransport, MotorDriver

with I2CTransport(bus_number=1) as transport:
    left_motor = MotorDriver(transport, address=0xFE)
    right_motor = MotorDriver(transport, address=0xFF)
    
    # Move both motors forward
    left_motor.forward(200)
    right_motor.forward(200)
```

### Error Handling

```python
from smart_i2c_motor_driver import (
    I2CTransport,
    MotorDriver,
    TransportError,
    InvalidSpeedError,
)

try:
    with I2CTransport() as transport:
        motor = MotorDriver(transport)
        motor.forward(200)
except TransportError as e:
    print(f"I2C communication error: {e}")
except InvalidSpeedError as e:
    print(f"Invalid speed value: {e}")
```

## Roadmap

- [ ] Add PID control support
- [ ] Implement encoder feedback
- [ ] Add motion profiling
- [ ] Support for SPI transport
- [ ] GUI control application

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.
