# Troubleshooting

Common issues and solutions for the Smart I2C Motor Driver.

## Installation Issues

### SMBus2 Import Error

**Problem**: `ImportError: No module named 'smbus2'`

**Solution**:
```bash
pip install smbus2
```

If that fails on Raspberry Pi:
```bash
sudo apt-get install python3-dev
pip install smbus2
```

### Click Not Found (CLI)

**Problem**: `ModuleNotFoundError: No module named 'click'`

**Solution**:
```bash
pip install smart-i2c-motor-driver[cli]
```

## Permission Issues

### Permission Denied on I2C

**Problem**: `PermissionError: [Errno 13] Permission denied: '/dev/i2c-1'`

**Solution**:

1. Add user to i2c group:
   ```bash
   sudo usermod -a -G i2c $USER
   ```

2. Log out and back in (or reboot)

3. Verify group membership:
   ```bash
   groups
   ```

4. Check i2c device permissions:
   ```bash
   ls -l /dev/i2c-*
   ```

### Root Required

**Problem**: Commands only work with `sudo`

**Solution**: Don't use `sudo`. Instead, fix permissions as shown above.

## I2C Communication Issues

### No I2C Device Found

**Problem**: `TransportError: Failed to open I2C bus`

**Solution**:

1. Enable I2C in raspi-config:
   ```bash
   sudo raspi-config
   # Interface Options -> I2C -> Enable
   ```

2. Reboot:
   ```bash
   sudo reboot
   ```

3. Verify I2C is loaded:
   ```bash
   lsmod | grep i2c
   ```

4. Check for I2C devices:
   ```bash
   i2cdetect -y 1
   ```

### Wrong Bus Number

**Problem**: Motor not responding

**Solution**:

Check which I2C bus your device is on:

```bash
# Try bus 0
i2cdetect -y 0

# Try bus 1
i2cdetect -y 1
```

Use the correct bus number:
```python
transport = I2CTransport(bus_number=0)  # or 1
```

### Device Not at Expected Address

**Problem**: `TransportError: Failed to write to I2C address`

**Solution**:

1. Scan for I2C devices:
   ```bash
   i2cdetect -y 1
   ```

2. Use the correct address in your code:
   ```python
   motor = MotorDriver(transport, address=0x10)  # Use detected address
   ```

## Motor Control Issues

### Motor Not Moving

**Possible Causes**:

1. **Wrong address**: Verify with `i2cdetect`
2. **Power supply**: Check motor controller power
3. **Connections**: Verify I2C SDA/SCL connections
4. **Speed too low**: Try higher speed values

**Debug Steps**:

```python
import logging
from smart_i2c_motor_driver import setup_logging

# Enable verbose logging
setup_logging(level=logging.DEBUG)

# Then run your code
motor.forward(200)
```

### Motor Moves Erratically

**Possible Causes**:

1. **Loose connections**: Check I2C wires
2. **Power issues**: Ensure stable power supply
3. **EMI interference**: Keep I2C wires short and away from motors
4. **Pull-up resistors**: I2C requires pull-ups (usually on controller)

**Solution**:

1. Check connections
2. Add 0.1µF capacitor near motor controller
3. Use shielded cables for longer runs
4. Verify 3.3V/5V level compatibility

### Motor Runs in Wrong Direction

**Problem**: Forward/backward reversed

**Solution**:

This is determined by motor wiring. Either:

1. Swap motor wires physically, or
2. Swap forward/backward in code:

```python
# If forward should be backward
motor.backward(200)  # Actually goes forward

# If backward should be forward
motor.forward(200)   # Actually goes backward
```

## Speed Issues

### Invalid Speed Error

**Problem**: `InvalidSpeedError: Speed must be between 0 and 255`

**Solution**:

Ensure speed is in valid range:

```python
# Wrong
motor.forward(-10)   # Negative
motor.forward(300)   # Too high

# Correct
motor.forward(0)     # Min speed
motor.forward(255)   # Max speed
```

### Motor Too Fast/Slow

**Problem**: Speed doesn't match expectations

**Solution**:

The speed value is PWM duty cycle (0-255):

```python
# Very slow
motor.forward(30)

# Slow
motor.forward(64)    # ~25%

# Medium
motor.forward(128)   # 50%

# Fast
motor.forward(192)   # ~75%

# Very fast
motor.forward(255)   # 100%
```

## Python Issues

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'smart_i2c_motor_driver'`

**Solution**:

1. Verify installation:
   ```bash
   pip list | grep smart-i2c
   ```

2. Reinstall if needed:
   ```bash
   pip install --force-reinstall smart-i2c-motor-driver
   ```

3. Check Python environment:
   ```bash
   which python
   python --version
   ```

### Type Errors

**Problem**: `TypeError: Speed must be an integer`

**Solution**:

Ensure you pass integers:

```python
# Wrong
motor.forward("200")   # String
motor.forward(200.5)   # Float

# Correct
motor.forward(200)     # Integer
motor.forward(int(200.5))  # Convert to int
```

## Hardware Issues

### I2C Not Available

**Problem**: `/dev/i2c-*` doesn't exist

**Solution**:

1. Enable I2C interface:
   ```bash
   sudo raspi-config
   # Interface Options -> I2C -> Enable
   ```

2. Load I2C kernel module:
   ```bash
   sudo modprobe i2c-dev
   ```

3. Make it permanent:
   ```bash
   echo "i2c-dev" | sudo tee -a /etc/modules
   ```

### Multiple Devices Conflict

**Problem**: Multiple I2C devices interfere

**Solution**:

1. Check all addresses are unique:
   ```bash
   i2cdetect -y 1
   ```

2. Use different addresses for each motor:
   ```python
   motor1 = MotorDriver(transport, address=0xFE)
   motor2 = MotorDriver(transport, address=0xFF)
   ```

## Debugging Tips

### Enable Debug Logging

```python
import logging
from smart_i2c_motor_driver import setup_logging

setup_logging(level=logging.DEBUG)
```

### Test I2C Manually

```bash
# Install i2c-tools
sudo apt-get install i2c-tools

# Scan bus
i2cdetect -y 1

# Read from device
i2cget -y 1 0xFE

# Write to device
i2cset -y 1 0xFE 0x01
```

### Minimal Test Program

```python
from smart_i2c_motor_driver import I2CTransport, MotorDriver, setup_logging
import logging

# Enable logging
setup_logging(level=logging.DEBUG)

try:
    # Create transport
    print("Creating transport...")
    transport = I2CTransport(bus_number=1)
    print("Transport created")
    
    # Create motor
    print("Creating motor...")
    motor = MotorDriver(transport, address=0xFE)
    print("Motor created")
    
    # Test motor
    print("Testing motor...")
    motor.forward(100)
    print("Motor started")
    
    input("Press Enter to stop...")
    motor.stop()
    print("Motor stopped")
    
    transport.close()
    print("Transport closed")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
```

## Getting Help

If you still have issues:

1. Check the [GitHub Issues](https://github.com/yourusername/smart-i2c-motor-driver/issues)
2. Enable debug logging and include output
3. Include your hardware setup details
4. Provide the full error traceback

## Common Error Messages

### `OSError: [Errno 121] Remote I/O error`

**Cause**: I2C device not responding

**Solution**: Check address with `i2cdetect`, verify connections and power

### `OSError: [Errno 16] Device or resource busy`

**Cause**: Another program is using the I2C bus

**Solution**: Close other programs accessing I2C

### `OSError: [Errno 2] No such file or directory: '/dev/i2c-1'`

**Cause**: I2C not enabled

**Solution**: Enable I2C in raspi-config and reboot

## Next Steps

- Review [Basic Usage](user-guide/basic-usage.md)
- Check [Installation Guide](installation.md)
- See [API Reference](reference/core.md)
