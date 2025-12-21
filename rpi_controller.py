"""
Raspberry Pi GPIO controller for physical access control.

Controls GPIO pins to trigger physical devices like door locks,
lights, and alarms.

Note: Requires RPi.GPIO package and Raspberry Pi hardware.
"""

try:
    import RPi.GPIO as GPIO

    # Use BCM pin numbering
    GPIO.setmode(GPIO.BCM)

    # Configure GPIO pin 18 as output for door control
    DOOR_PIN = 18
    GPIO.setup(DOOR_PIN, GPIO.OUT)

    def open_door() -> None:
        """Activate door lock to open."""
        GPIO.output(DOOR_PIN, GPIO.HIGH)
        print("Door opened")

    def close_door() -> None:
        """Deactivate door lock to close."""
        GPIO.output(DOOR_PIN, GPIO.LOW)
        print("Door closed")

    def cleanup() -> None:
        """Clean up GPIO resources."""
        GPIO.cleanup()

    # Example usage
    if __name__ == "__main__":
        open_door()

except ImportError:
    print("Warning: RPi.GPIO not available. Running on non-Raspberry Pi system.")
    print("GPIO control disabled.")

    def open_door() -> None:
        """Stub function when GPIO unavailable."""
        print("Simulated: Door would open")

    def close_door() -> None:
        """Stub function when GPIO unavailable."""
        print("Simulated: Door would close")

    def cleanup() -> None:
        """Stub function when GPIO unavailable."""
        pass
