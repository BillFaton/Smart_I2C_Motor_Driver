"""I2C transport implementation using smbus2."""

import logging
import time
from typing import Optional

from .base import Transport, TransportError

logger = logging.getLogger(__name__)


class I2CTransport(Transport):
    """I2C transport implementation using smbus2.
    
    This transport manages a shared I2C bus that can be used by multiple
    motor driver instances.
    
    Args:
        bus_number: The I2C bus number (typically 1 on Raspberry Pi)
        
    Example:
        >>> transport = I2CTransport(bus_number=1)
        >>> transport.write_byte(0xFE, 0x01)
        >>> transport.close()
    """
    
    def __init__(self, bus_number: int = 1):
        """Initialize the I2C transport.
        
        Args:
            bus_number: The I2C bus number (default: 1)
            
        Raises:
            TransportError: If the I2C bus cannot be opened
        """
        self.bus_number = bus_number
        self._bus: Optional[object] = None
        self._open_bus()
        
    def _open_bus(self) -> None:
        """Open the I2C bus.
        
        Raises:
            TransportError: If smbus2 is not installed or bus cannot be opened
        """
        try:
            from smbus2 import SMBus
            self._bus = SMBus(self.bus_number)
            logger.info(f"Opened I2C bus {self.bus_number}")
        except ImportError:
            raise TransportError(
                "smbus2 is not installed. Install it with: pip install smbus2"
            )
        except Exception as e:
            raise TransportError(
                f"Failed to open I2C bus {self.bus_number}: {e}"
            )
    
    def write_byte(self, address: int, data: int) -> None:
        """Write a single byte to the specified I2C address.
        
        Args:
            address: The I2C slave address (7-bit, 0x00-0x7F)
            data: The byte to write (0-255)
            
        Raises:
            TransportError: If communication fails
            ValueError: If address or data is out of range
        """
        if not 0x00 <= address <= 0x7F:
            raise ValueError(f"I2C address must be 0x00-0x7F, got 0x{address:02X}")
        
        if not 0 <= data <= 255:
            raise ValueError(f"Data must be 0-255, got {data}")
        
        if self._bus is None:
            raise TransportError("I2C bus is not open")
        
        try:
            self._bus.write_byte(address, data)
            logger.debug(f"Wrote 0x{data:02X} to address 0x{address:02X}")
        except Exception as e:
            raise TransportError(
                f"Failed to write to I2C address 0x{address:02X}: {e}"
            )
    
    def close(self) -> None:
        """Close the I2C bus and release resources."""
        if self._bus is not None:
            try:
                self._bus.close()
                logger.info(f"Closed I2C bus {self.bus_number}")
            except Exception as e:
                logger.warning(f"Error closing I2C bus: {e}")
            finally:
                self._bus = None
    
    def __del__(self):
        """Ensure the bus is closed when the object is destroyed."""
        self.close()
