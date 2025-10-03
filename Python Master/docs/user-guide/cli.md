# CLI Usage

The Smart I2C Motor Driver includes a command-line interface for quick motor testing and control.

## Installation

The CLI requires the `click` package. Install with:

```bash
pip install smart-i2c-motor-driver[cli]
```

## Basic Commands

### Forward

Run motor forward at specified speed:

```bash
smart-motor forward 200
```

With duration (in seconds):

```bash
smart-motor forward 200 --duration 2.0
```

### Backward

Run motor backward at specified speed:

```bash
smart-motor backward 150
```

With duration:

```bash
smart-motor backward 150 --duration 3.0
```

### Stop

Stop the motor:

```bash
smart-motor stop
```

### Info

Display motor driver information:

```bash
smart-motor info
```

## Global Options

### Bus Number

Specify I2C bus number (default: 1):

```bash
smart-motor --bus 1 forward 200
```

Short form:

```bash
smart-motor -b 1 forward 200
```

### Motor Address

Specify motor I2C address (default: 0xFE):

```bash
smart-motor --address 0xFF forward 200
```

Short form:

```bash
smart-motor -a 0xFF forward 200
```

### Verbose Logging

Enable verbose logging:

```bash
smart-motor --verbose forward 200
```

Short form:

```bash
smart-motor -v forward 200
```

## Examples

### Basic Testing

Test motor forward:

```bash
smart-motor forward 128
```

Test motor backward:

```bash
smart-motor backward 128
```

### Timed Operation

Run forward for 5 seconds:

```bash
smart-motor forward 200 -d 5.0
```

Run backward for 3 seconds:

```bash
smart-motor backward 150 -d 3.0
```

### Multiple Motors

Control first motor:

```bash
smart-motor --address 0xFE forward 200
```

Control second motor:

```bash
smart-motor --address 0xFF forward 180
```

### Different Bus

Use bus 0:

```bash
smart-motor --bus 0 forward 200
```

### Debug Mode

Run with verbose logging:

```bash
smart-motor -v forward 200
```

## Scripts and Automation

### Simple Test Script

```bash
#!/bin/bash
# test-motor.sh

# Test forward
smart-motor forward 200 -d 2
sleep 1

# Test backward  
smart-motor backward 150 -d 2
sleep 1

# Stop
smart-motor stop
```

### Two Motor Script

```bash
#!/bin/bash
# test-two-motors.sh

# Start both motors
smart-motor -a 0xFE forward 200 -d 2 &
smart-motor -a 0xFF forward 200 -d 2 &
wait

# Stop both
smart-motor -a 0xFE stop
smart-motor -a 0xFF stop
```

## Troubleshooting

### Permission Denied

If you get permission errors:

```bash
# Add user to i2c group
sudo usermod -a -G i2c $USER

# Log out and back in, then test
smart-motor info
```

### Command Not Found

If `smart-motor` command is not found:

1. Ensure CLI dependencies are installed:
   ```bash
   pip install smart-i2c-motor-driver[cli]
   ```

2. Check if it's in your PATH:
   ```bash
   which smart-motor
   ```

3. Try using Python module directly:
   ```bash
   python -m app.cli forward 200
   ```

### Wrong Bus/Address

Verify I2C devices:

```bash
i2cdetect -y 1
```

This shows all devices on bus 1.

## Help

Get help for any command:

```bash
# General help
smart-motor --help

# Command-specific help
smart-motor forward --help
smart-motor backward --help
smart-motor stop --help
```

## Output Format

The CLI provides clear feedback:

```
$ smart-motor forward 200
Motor running forward at speed 200

$ smart-motor forward 200 -d 2
Motor running forward at speed 200
Motor stopped

$ smart-motor stop
Motor stopped

$ smart-motor info
Smart I2C Motor Driver
I2C Bus: 1
Address: 0xFE
```

## Error Messages

The CLI provides descriptive error messages:

```
$ smart-motor forward 300
Error: Speed must be between 0 and 255, got 300

$ smart-motor -a 0x80 forward 200
Error: I2C address must be 0x00-0x7F, got 0x80
```

## Integration with Other Tools

### systemd Service

Create a motor control service:

```ini
# /etc/systemd/system/motor-test.service
[Unit]
Description=Motor Test Service
After=network.target

[Service]
Type=oneshot
User=pi
ExecStart=/usr/local/bin/smart-motor forward 200 -d 10
ExecStop=/usr/local/bin/smart-motor stop

[Install]
WantedBy=multi-user.target
```

### Cron Job

Schedule motor operations:

```cron
# Run motor every hour for 1 minute
0 * * * * /usr/local/bin/smart-motor forward 150 -d 60
```

## Next Steps

- [Basic Usage](basic-usage.md) - Use the Python API
- [API Reference](../reference/core.md) - Complete API documentation
- [Troubleshooting](../troubleshooting.md) - Common issues
