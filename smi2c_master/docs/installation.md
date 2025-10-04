# Installation

## Requirements

- Python 3.13 or higher
- I2C-enabled hardware (e.g., Raspberry Pi)
- I2C device permissions

## Basic Installation

### Using pip

Install the package from PyPI:

```bash
pip install smart-i2c-motor-driver
```

### Using uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer. Install it first:

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using pip
pip install uv
```

Then install the package:

```bash
uv pip install smart-i2c-motor-driver
```

uv is significantly faster than pip for package installation.

## Installation with Optional Features

### CLI Support

To use the command-line interface:

```bash
pip install smart-i2c-motor-driver[cli]
```

### Development Tools

To install development dependencies:

```bash
pip install smart-i2c-motor-driver[dev]
```

### Documentation Tools

To build documentation locally:

```bash
pip install smart-i2c-motor-driver[docs]
```

### All Optional Features

To install everything:

```bash
pip install smart-i2c-motor-driver[all]
```

## Installation from Source

Clone the repository:

```bash
git clone https://github.com/Mahudjro369/smart-i2c-motor-driver.git
cd smart-i2c-motor-driver/Python\ Master
```

### Using pip

Install in development mode:

```bash
pip install -e .
```

Or with all optional dependencies:

```bash
pip install -e .[all]
```

### Using uv (Faster)

First, create a virtual environment:

```bash
uv venv
source .venv/bin/activate  # On macOS/Linux
# Or on Windows: .venv\Scripts\activate
```

Install in development mode:

```bash
uv pip install -e .
```

Or with all optional dependencies:

```bash
# On macOS/Linux (quote for zsh)
uv pip install -e '.[all]'

# On Windows
uv pip install -e .[all]
```

Or install without a virtual environment:

```bash
uv pip install --system -e .
```

## Hardware Setup

### Raspberry Pi I2C Configuration

1. Enable I2C interface:
   ```bash
   sudo raspi-config
   # Navigate to: Interface Options -> I2C -> Enable
   ```

2. Install I2C tools:
   ```bash
   sudo apt-get update
   sudo apt-get install i2c-tools
   ```

3. Add user to i2c group:
   ```bash
   sudo usermod -a -G i2c $USER
   ```
   (Log out and back in for changes to take effect)

4. Verify I2C is working:
   ```bash
   i2cdetect -y 1
   ```

### I2C Bus Numbers

- **Raspberry Pi 3/4/5**: Bus 1 (default)
- **Raspberry Pi 1 (Rev 2)**: Bus 1
- **Raspberry Pi 1 (Rev 1)**: Bus 0
- **Other platforms**: Check your hardware documentation

## Verification

Verify the installation:

```python
import smi2c_master
print(smi2c_master.__version__)
```

Run tests (if dev dependencies installed):

```bash
pytest
```

## Troubleshooting

### Permission Denied

If you get "Permission denied" errors when accessing I2C:

1. Ensure you're in the i2c group:
   ```bash
   groups
   ```

2. If not, add yourself and reboot:
   ```bash
   sudo usermod -a -G i2c $USER
   sudo reboot
   ```

### Module Not Found

If Python can't find the module:

1. Ensure you're using the correct Python environment
2. Try installing with `--user` flag:
   ```bash
   pip install --user smart-i2c-motor-driver
   ```

### SMBus2 Installation Issues

If smbus2 installation fails:

```bash
# On Debian/Ubuntu
sudo apt-get install python3-dev

# Then retry
pip install smbus2
```

## Next Steps

- [Getting Started Guide](getting-started.md)
- [Basic Usage](user-guide/basic-usage.md)
