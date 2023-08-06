"""
These classes perform simple operations on pins.
"""
try:
    import RPi.GPIO as GPIO
except:
    import Mock.GPIO as GPIO

import logging
import math
from whendo.core.action import Action

logger = logging.getLogger(__name__)


class SetPin(Action):
    """
    Sets the pin state to HIGH if <on> is True, to LOW otherwise.
    """

    pin: int
    on: bool # accepts, 0, 1, False, True

    def description(self):
        return f"This action sets pin ({self.pin}) state to ({'GPIO.HIGH' if self.on else 'GPIO.LOW'})."

    def execute(self, tag: str = None, scheduler_info: dict = None):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.HIGH if self.on else GPIO.LOW)
        return self.on


class PinState(Action):
    """
    Returns True if the pin state is HIGH, 0 if the pin state is LOW.
    """

    pin: int
    pin_state: str = "pin_state"  # for Action deserialization

    def description(self):
        return f"This action returns True if the pin state is HIGH, False if LOW."

    def execute(self, tag: str = None, scheduler_info: dict = None):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.OUT)
        return GPIO.input(self.pin) == GPIO.HIGH


class TogglePin(Action):
    """
    Sets the pin state to HIGH if LOW, to LOW if HIGH. Returns True
    if final state is HIGH, False if final state is LOW.
    """

    pin: int

    def description(self):
        return f"This action sets pin ({self.pin}) state to GPIO.HIGH if LOW, to GPIO.LOW if HIGH. Returns True if final state is HIGH, False if final state is LOW."

    def execute(self, tag: str = None, scheduler_info: dict = None):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.OUT)
        state = not GPIO.input(self.pin)
        GPIO.output(self.pin, state)
        return state == GPIO.HIGH


class CleanupPins(Action):
    """
    Clean up the pins. See the docs for GPIO.cleanup().
    """

    cleanup_pins: str = "cleanup_pins"

    def description(self):
        return f"This action executes GPIO.cleanup."

    def execute(self, tag: str = None, scheduler_info: dict = None):
        GPIO.cleanup()
        return False
