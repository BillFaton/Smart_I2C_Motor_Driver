"""Example usage of the Smart I2C Motor Driver library."""

import time
import logging
from smi2c_master import (
    I2CTransport,
    MotorDriver,
    setup_logging,
    TransportError,
)


def single_motor_example():
    """Example: Control a single motor."""
    print("=== Single Motor Example ===\n")
    
    try:
        with I2CTransport(bus_number=1) as transport:
            motor = MotorDriver(transport, address=0xFE)
            
            print("Moving forward at speed 200...")
            motor.forward(200)
            time.sleep(2)
            
            print("Moving backward at speed 150...")
            motor.backward(150)
            time.sleep(2)
            
            print("Stopping motor...")
            motor.stop()
            print("Done!\n")
            
    except TransportError as e:
        print(f"Error: {e}\n")


def multiple_motors_example():
    """Example: Control multiple motors."""
    print("=== Multiple Motors Example ===\n")
    
    try:
        with I2CTransport(bus_number=1) as transport:
            left_motor = MotorDriver(transport, address=0xFE)
            right_motor = MotorDriver(transport, address=0xFF)
            
            print("Moving both motors forward...")
            left_motor.forward(200)
            right_motor.forward(200)
            time.sleep(2)
            
            print("Turning right (left forward, right backward)...")
            left_motor.forward(200)
            right_motor.backward(200)
            time.sleep(1)
            
            print("Moving both motors backward...")
            left_motor.backward(150)
            right_motor.backward(150)
            time.sleep(2)
            
            print("Stopping both motors...")
            left_motor.stop()
            right_motor.stop()
            print("Done!\n")
            
    except TransportError as e:
        print(f"Error: {e}\n")


def motor_properties_example():
    """Example: Access motor properties."""
    print("=== Motor Properties Example ===\n")
    
    try:
        with I2CTransport(bus_number=1) as transport:
            motor = MotorDriver(transport, address=0xFE)
            
            print(f"Motor address: 0x{motor.address:02X}")
            print(f"Is active: {motor.is_active}")
            print(f"Current speed: {motor.current_speed}\n")
            
            print("Starting motor...")
            motor.forward(128)
            
            print(f"Is active: {motor.is_active}")
            print(f"Current speed: {motor.current_speed}\n")
            
            motor.stop()
            print("Motor stopped")
            print(f"Is active: {motor.is_active}")
            print(f"Current speed: {motor.current_speed}\n")
            
    except TransportError as e:
        print(f"Error: {e}\n")


def main():
    """Run all examples."""
    print("\n" + "="*50)
    print("Smart I2C Motor Driver - Examples")
    print("="*50 + "\n")
    
    # Enable logging
    setup_logging(level=logging.INFO)
    
    # Run examples
    try:
        single_motor_example()
        
        # Uncomment to run multiple motors example
        # multiple_motors_example()
        
        # Uncomment to run properties example
        # motor_properties_example()
        
    except KeyboardInterrupt:
        print("\n\nStopped by user")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
