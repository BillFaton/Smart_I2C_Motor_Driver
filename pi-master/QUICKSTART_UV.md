# Quick Start with uv

This guide shows you how to quickly get started using [uv](https://github.com/astral-sh/uv), the fast Python package installer.

## Why uv?

- ⚡ **10-100x faster** than pip
- 🔒 Consistent, reproducible installs
- 🎯 Modern Python package management

## Installation

### 1. Install uv

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```bash
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Or using pip:**
```bash
pip install uv
```

### 2. Create Virtual Environment

```bash
cd "Python Master"
uv venv
source .venv/bin/activate  # On macOS/Linux
# Or on Windows: .venv\Scripts\activate
```

### 3. Install the Package

**Basic installation:**
```bash
uv pip install -e .
```

**With all features:**
```bash
# On macOS/Linux (zsh/bash)
uv pip install -e '.[all]'

# On Windows
uv pip install -e .[all]
```

**For specific features:**
```bash
# CLI only
uv pip install -e '.[cli]'

# Development tools
uv pip install -e '.[dev]'

# Documentation tools
uv pip install -e '.[docs]'
```

**Alternative (without virtual environment):**
```bash
uv pip install --system -e .
```

## Running Examples

```bash
# Run the example script
python main.py

# Or using uv run (if configured)
uv run python main.py
```

## Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=smi2c_master --cov-report=html
```

## Building Documentation

```bash
# Serve docs locally
mkdocs serve

# Build static site
mkdocs build
```

## Using the CLI

```bash
# Basic motor control
smart-motor forward 200
smart-motor backward 150
smart-motor stop

# With options
smart-motor --bus 1 --address 0xFE forward 200 --duration 2.0
```

## Usage Example

```python
from smi2c_master import I2CTransport, MotorDriver

# Create transport and motor
with I2CTransport(bus_number=1) as transport:
    motor = MotorDriver(transport, address=0xFE)
    
    # Control the motor
    motor.forward(200)
    motor.stop()
```

## GitHub Pages Documentation

After pushing to GitHub, documentation will automatically deploy to:
```
https://Mahudjro369.github.io/smart-i2c-motor-driver
```

See [docs/README.md](docs/README.md) for setup instructions.

## Troubleshooting

### uv not found
Restart your shell after installation:
```bash
source ~/.bashrc  # or ~/.zshrc
```

### Permission issues on Raspberry Pi
```bash
sudo usermod -a -G i2c $USER
# Log out and back in
```

### Import errors
Ensure you're in the correct directory:
```bash
cd "Python Master"
uv pip install -e .
```

## Next Steps

- 📖 Read the [full documentation](docs/index.md)
- 🚀 Check [getting-started.md](docs/getting-started.md)
- 🔧 See [basic-usage.md](docs/user-guide/basic-usage.md)
- 💡 View [examples in main.py](main.py)
