"""Command-line interface for Smart I2C Motor Driver."""

import logging
import sys
import time
from typing import Optional

import click

from smart_i2c_motor_driver import (
    I2CTransport,
    InvalidAddressError,
    InvalidSpeedError,
    MotorDriver,
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
    default=0xFE,
    help="Motor I2C address (default: 0xFE)",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose logging",
)
@click.pass_context
def cli(ctx, bus: int, address: int, verbose: bool):
    """Smart I2C Motor Driver CLI.
    
    Control motors connected via I2C using the Smart Driver Protocol.
    """
    # Setup logging
    level = logging.DEBUG if verbose else logging.INFO
    setup_logging(level=level)
    
    # Store configuration in context
    ctx.ensure_object(dict)
    ctx.obj["bus"] = bus
    ctx.obj["address"] = address


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
            motor = MotorDriver(transport, ctx.obj["address"])
            motor.forward(speed)
            click.echo(f"Motor running forward at speed {speed}")
            
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
            motor = MotorDriver(transport, ctx.obj["address"])
            motor.backward(speed)
            click.echo(f"Motor running backward at speed {speed}")
            
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
            motor = MotorDriver(transport, ctx.obj["address"])
            motor.stop()
            click.echo("Motor stopped")
    except (TransportError, InvalidAddressError) as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.pass_context
def info(ctx):
    """Display motor driver information."""
    click.echo("Smart I2C Motor Driver")
    click.echo(f"I2C Bus: {ctx.obj['bus']}")
    click.echo(f"Address: 0x{ctx.obj['address']:02X}")


def main():
    """Entry point for the CLI."""
    cli(obj={})


if __name__ == "__main__":
    main()
