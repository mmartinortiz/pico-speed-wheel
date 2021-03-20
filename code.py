"""
Adafruit CircuitPython 6.2.0-beta.2
Raspberry Pi Pico with rp2040
"""
import time

import board
import usb_hid
from adafruit_hid.gamepad import Gamepad
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = True

print("Initializing the gamepad")
# Create a gamepad for HID simulation
gp = Gamepad(usb_hid.devices)

# Other pins can also be set to output
# for detecting buttons.
out = DigitalInOut(board.GP16)
out.direction = Direction.OUTPUT
out.value = True

buttons = {
    i + 1: {"device": DigitalInOut(device), "pressed": False}
    for i, device in enumerate(
        [
            # Buttons in the steering wheel, from 1 to 6
            board.GP4,
            board.GP9,
            board.GP2,
            board.GP3,
            board.GP6,
            board.GP5,
            # Buttons in the gear lever, from 7 to 10
            board.GP11,
            board.GP13,
            board.GP12,
            board.GP7,
        ],
    )
}

steering_wheel = AnalogIn(board.A0)
gear_lever = AnalogIn(board.A1)

for _, button in buttons.items():
    button["device"].direction = Direction.INPUT
    button["device"].pull = Pull.DOWN

print("Setup finished")


def calibrate_analog_input(device: AnalogIn) -> None:
    """Helper function for calibrating an analog device. It prints in the terminal
    the lower and upper limits that an analog device can provide in the extremes.

    Args:
        device (AnalogIn): Device that provides the value
    """
    max_value = 0
    min_value = 65000

    print("For calibration, start moving the device up/down left/right")
    start = time.monotonic()
    keep_doing = True
    while keep_doing:
        value = device.value
        max_value = value if value > max_value else max_value
        min_value = value if value < min_value else min_value

        keep_doing = False if time.monotonic() - start > 5 else keep_doing

    print(f"Calibration done. Max: {max_value} || Min: {min_value}")


def scale_voltage(
    voltage: float,
    min_voltage: int,
    max_voltage: int,
    lower_limit: int = -127,
    upper_limit: int = 127,
) -> int:
    """Given a voltage, scales the output to values between `a` and `b`. Requires the maximum
    and minimum values that `voltage` can have.

    Args:
        voltage (float): Value to be scaled
        min_voltage (int): Minimum voltage possible
        max_voltage (int): Maximum voltage possible
        lower_limit (int, optional): Lower limit for the scale. Defaults to -127.
        upper_limit (int, optional): Upper limit for the scale. Defaults to 127.

    Returns:
        int: Scaled value for the voltage
    """
    result = (upper_limit - lower_limit) * (
        (voltage - min_voltage) / (max_voltage - min_voltage)
    ) + lower_limit

    result = upper_limit if result > upper_limit else result
    result = lower_limit if result < lower_limit else result

    return int(result)


def get_gear_position(device: AnalogIn) -> int:
    """Returns the current gear lever position, between -127 and 127

    Args:
        device (AnalogIn): Analog device that represents the Gear lever

    Returns:
        int: Value between -127 and 127
    """
    return scale_voltage(device.value, min_voltage=16720, max_voltage=50016)


def get_wheel_position(device: AnalogIn) -> int:
    """Returns the current Wheel position, value between -127 and 127

    Args:
        device (AnalogIn): Analog device representing the wheel

    Returns:
        int: Scaled wheel value, between -127 and 127
    """
    return scale_voltage(device.value, min_voltage=3520, max_voltage=61712)


# calibrate_analog_input(steering_wheel)
while True:
    for idx, button in buttons.items():
        if not button["device"].value and button["pressed"]:
            button["pressed"] = False
            print(f"Button {idx} Released!")
            gp.release_buttons(idx)

        if button["device"].value and not button["pressed"]:
            button["pressed"] = True
            print(f"Button {idx} pressed!")
            gp.press_buttons(idx)

    gear_position = get_gear_position(gear_lever)
    wheel_position = get_wheel_position(steering_wheel)

    gp.move_joysticks(x=wheel_position, y=gear_position)
