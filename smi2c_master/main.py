"""Example usage of the Smart I2C Motor Driver library."""

import time
import logging
from smi2c_master import (
    I2CTransport,
    MotorDriver,
    MotorID,
    Direction,
    MotorState,
    setup_logging,
    TransportError,
)
from smi2c_master.transports.base import Transport

class MockTransport(Transport):
    """Mock transport for testing without actual I2C hardware."""
    
    def __init__(self):
        self.written_data = []
    
    def write_byte(self, address: int, data: int) -> None:
        self.written_data.append((address, data))
        print(f"Mock I2C: Write 0x{data:02X} to address 0x{address:02X}")
    
    def close(self) -> None:
        pass


def single_motor_example():
    """Example: Control a single motor."""
    print("=== Single Motor Example ===\n")
    
    try:
        with I2CTransport(bus_number=1) as transport:
            motor = MotorDriver(transport, MotorID.MOTOR_0)
            
            print("Moving Motor 0 forward at speed 200...")
            motor.forward(200)
            time.sleep(2)
            
            print("Moving Motor 0 backward at speed 150...")
            motor.backward(150)
            time.sleep(2)
            
            print("Stopping Motor 0...")
            motor.stop()
            print("Done!\n")
            
    except TransportError as e:
        print(f"Error: {e}\n")


def multiple_motors_example():
    """Example: Control multiple motors on the same slave."""
    print("=== Multiple Motors Example ===\n")
    
    try:
        with I2CTransport(bus_number=1) as transport:
            motor0 = MotorDriver(transport, MotorID.MOTOR_0)  # Motor 0 on slave 0x7F
            motor1 = MotorDriver(transport, MotorID.MOTOR_1)  # Motor 1 on slave 0x7F
            
            print("Moving both motors forward...")
            motor0.forward(200)
            motor1.forward(200)
            time.sleep(2)
            
            print("Turning right (Motor 0 forward, Motor 1 backward)...")
            motor0.forward(200)
            motor1.backward(200)
            time.sleep(1)
            
            print("Moving both motors backward...")
            motor0.backward(150)
            motor1.backward(150)
            time.sleep(2)
            
            print("Stopping both motors...")
            motor0.stop()
            motor1.stop()
            print("Done!\n")
            
    except TransportError as e:
        print(f"Error: {e}\n")


def motor_properties_example():
    """Example: Access motor properties."""
    print("=== Motor Properties Example ===\n")
    
    try:
        with I2CTransport(bus_number=1) as transport:
            motor = MotorDriver(transport, MotorID.MOTOR_1)
            
            print(f"Motor address: 0x{motor.address:02X}")
            print(f"Motor ID: {motor.motor_id.value}")
            print(f"Is active: {motor.is_active}")
            print(f"Current speed: {motor.current_speed}\n")
            
            print("Starting Motor 1...")
            motor.forward(128)
            
            print(f"Is active: {motor.is_active}")
            print(f"Current speed: {motor.current_speed}\n")
            
            motor.stop()
            print("Motor 1 stopped")
            print(f"Is active: {motor.is_active}")
            print(f"Current speed: {motor.current_speed}\n")
            
    except TransportError as e:
        print(f"Error: {e}\n")


def protocol_verification_test():
    """Test the 4-step protocol implementation matches Arduino."""
    print("=== Protocol Verification Test ===\n")
    print("Testing new 4-step protocol implementation...")
    print("=" * 50)
    
    # Test Motor 0 Forward
    transport = MockTransport()
    motor0 = MotorDriver(transport, MotorID.MOTOR_0)
    
    print(f"Motor ID: {motor0.motor_id.value}")
    print(f"Address: 0x{motor0.address:02X}")
    print()
    
    print("Testing forward command (Motor 0, speed 200):")
    motor0.forward(200)
    expected = [(0x7F, 0x00), (0x7F, 0x01), (0x7F, 0x00), (0x7F, 200)]
    print(f"Expected: {expected}")
    print(f"Actual:   {transport.written_data}")
    match1 = transport.written_data == expected
    print(f"Match: {match1}")
    print()
    
    # Test Motor 1 Backward
    transport = MockTransport()
    motor1 = MotorDriver(transport, MotorID.MOTOR_1)
    
    print("Testing backward command (Motor 1, speed 150):")
    motor1.backward(150)
    expected = [(0x7F, 0x01), (0x7F, 0x01), (0x7F, 0x01), (0x7F, 150)]
    print(f"Expected: {expected}")
    print(f"Actual:   {transport.written_data}")
    match2 = transport.written_data == expected
    print(f"Match: {match2}")
    print()
    
    # Test Motor 0 Stop
    transport = MockTransport()
    motor0 = MotorDriver(transport, MotorID.MOTOR_0)
    
    print("Testing stop command (Motor 0):")
    motor0.stop()
    expected = [(0x7F, 0x00), (0x7F, 0x00), (0x7F, 0x00), (0x7F, 0)]
    print(f"Expected: {expected}")
    print(f"Actual:   {transport.written_data}")
    match3 = transport.written_data == expected
    print(f"Match: {match3}")
    print()
    
    if match1 and match2 and match3:
        print("✅ All tests match expected Arduino protocol!")
    else:
        print("❌ Some tests failed!")
    print()


def main():
    """Run all examples and tests."""
    print("\n" + "="*50)
    print("Smart I2C Motor Driver - Examples & Tests")
    print("="*50 + "\n")
    
    # Enable logging
    setup_logging(level=logging.WARNING)  # Reduce noise for testing
    
    # Run examples and tests
    try:
        # First run the protocol verification test (works without hardware)
        protocol_verification_test()
        
        # Uncomment to test with actual hardware
        while True:
            # single_motor_example()
            multiple_motors_example()
            # motor_properties_example()
        
    except KeyboardInterrupt:
        print("\n\nStopped by user")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
