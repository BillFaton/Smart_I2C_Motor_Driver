"""Base transport interface for I2C motor driver communication."""

from abc import ABC, abstractmethod
from typing import Optional


class Transport(ABC):
    """Abstract base class for transport implementations.
    
    This defines the interface that all transport implementations must follow.
    """
    
    @abstractmethod
    def write_byte(self, address: int, data: int) -> None:
        """Write a single byte to the specified I2C address.
        
        Args:
            address: The I2C slave address (7-bit)
            data: The byte to write (0-255)
            
        Raises:
            TransportError: If communication fails
        """
        pass
    
    @abstractmethod
    def close(self) -> None:
        """Close the transport and release resources."""
        pass
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
        return False


class TransportError(Exception):
    """Base exception for transport-related errors."""
    pass
