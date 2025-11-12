"""Command-line interface for Smart I2C Motor Driver."""

import logging
import sys
import time
from typing import Optional

import click

from smi2c_master import (
    I2CTransport,
    InvalidAddressError,
    InvalidSpeedError,
    MotorDriver,
    MotorID,
    TransportError,
    setup_logging,
)


@click.group()
@click.option(
    "--bus",
    "-b",
    type=int,
    default=1,
    help="I2C bus number (default: 1)",
)
@click.option(
    "--address",
    "-a",
    type=lambda x: int(x, 0),
    default=0x7F,
    help="Motor I2C slave address (default: 0x7F)",
)
@click.option(
    "--motor",
    "-m",
    type=click.Choice(["0", "1"]),
    default="0",
    help="Motor ID: 0 or 1 (default: 0)",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose logging",
)
@click.pass_context
def cli(ctx, bus: int, address: int, motor: str, verbose: bool):
    """Smart I2C Motor Driver CLI.
    
    Control motors connected via I2C using the Smart Driver Protocol (4-step).
    """
    # Setup logging
    level = logging.DEBUG if verbose else logging.INFO
    setup_logging(level=level)
    
    # Convert motor ID string to MotorID enum
    motor_id = MotorID.MOTOR_0 if motor == "0" else MotorID.MOTOR_1
    
    # Store configuration in context
    ctx.ensure_object(dict)
    ctx.obj["bus"] = bus
    ctx.obj["address"] = address
    ctx.obj["motor_id"] = motor_id


@cli.command()
@click.argument("speed", type=click.IntRange(0, 255))
@click.option(
    "--duration",
    "-d",
    type=float,
    help="Run for specified duration in seconds",
)
@click.pass_context
def forward(ctx, speed: int, duration: Optional[float]):
    """Run motor forward at specified SPEED (0-255)."""
    try:
        with I2CTransport(ctx.obj["bus"]) as transport:
            motor = MotorDriver(transport, ctx.obj["motor_id"], ctx.obj["address"])
            motor.forward(speed)
            click.echo(f"Motor {ctx.obj['motor_id'].value} running forward at speed {speed}")
            
            if duration:
                time.sleep(duration)
                motor.stop()
                click.echo("Motor stopped")
    except (TransportError, InvalidSpeedError, InvalidAddressError) as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("speed", type=click.IntRange(0, 255))
@click.option(
    "--duration",
    "-d",
    type=float,
    help="Run for specified duration in seconds",
)
@click.pass_context
def backward(ctx, speed: int, duration: Optional[float]):
    """Run motor backward at specified SPEED (0-255)."""
    try:
        with I2CTransport(ctx.obj["bus"]) as transport:
            motor = MotorDriver(transport, ctx.obj["motor_id"], ctx.obj["address"])
            motor.backward(speed)
            click.echo(f"Motor {ctx.obj['motor_id'].value} running backward at speed {speed}")
            
            if duration:
                time.sleep(duration)
                motor.stop()
                click.echo("Motor stopped")
    except (TransportError, InvalidSpeedError, InvalidAddressError) as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.pass_context
def stop(ctx):
    """Stop the motor."""
    try:
        with I2CTransport(ctx.obj["bus"]) as transport:
            motor = MotorDriver(transport, ctx.obj["motor_id"], ctx.obj["address"])
            motor.stop()
            click.echo(f"Motor {ctx.obj['motor_id'].value} stopped")
    except (TransportError, InvalidAddressError) as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.pass_context
def info(ctx):
    """Display motor driver information."""
    click.echo("Smart I2C Motor Driver (4-step protocol)")
    click.echo(f"I2C Bus: {ctx.obj['bus']}")
    click.echo(f"Slave Address: 0x{ctx.obj['address']:02X}")
    click.echo(f"Motor ID: {ctx.obj['motor_id'].value}")


def main():
    """Entry point for the CLI."""
    cli(obj={})


if __name__ == "__main__":
    main()
