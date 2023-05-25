import time
import board
import busio
from adafruit_mcp230xx.mcp23017 import MCP23017

class GPIO:
    def __init__(self, i2c_bus, expander_type=MCP23017):
        self.mcp = expander_type(i2c_bus)

    def setup(self, pin, mode, pull_up_down=None):
        self.pin = self.mcp.get_pin(pin)
        if mode == 'OUT':
            self.pin.switch_to_output()
        elif mode == 'IN':
            self.pin.switch_to_input(pull=pull_up_down)

    def output(self, pin, value):
        self.pin = self.mcp.get_pin(pin)
        self.pin.value = value

    def input(self, pin):
        self.pin = self.mcp.get_pin(pin)
        return self.pin.value

    def cleanup(self):
        pass

    def setwarnings(self, bool):
        pass

    def __repr__(self):
        return "GPIO(pin={}, value={})".format(self.pin, self.pin.value)

    def __str__(self):
        return "GPIO(pin={}, value={})".format(self.pin, self.pin.value)


i2c = busio.I2C(board.SCL, board.SDA)
gpio = GPIO(i2c)

# Setup pin 0 as an output
gpio.setup(0, 'OUT')

# Setup pin 1 as an input with a pull-up resistor enabled
gpio.setup(1, 'IN', pull_up_down=True)

# Now loop blinking the pin 0 output and reading the state of pin 1 input
while True:
    # Blink pin 0 on and then off
    gpio.output(0, True)
    time.sleep(0.5)
    gpio.output(0, False)
    time.sleep(0.5)
    # Read pin 1 and print its state
    print("Pin 1 is at a high level: {0}".format(gpio.input(1)))
