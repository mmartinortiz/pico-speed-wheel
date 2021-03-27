# The Pico Speed Wheel

This is a short story about how I used a Raspberry Pi Pico for "resurrecting" a 1996 Speed Wheel DB15 GamePad, including the code to bring to a new life your own Speed Wheel. You can also find this project in [Make:Projects](https://makeprojects.com/project/reuse-your-old-db15-gamepad-thanks-to-a-raspberry-pi-pico)

- [The Pico Speed Wheel](#the-pico-speed-wheel)
  - [The Speed Wheel](#the-speed-wheel)
  - [The new wiring](#the-new-wiring)
  - [The code](#the-code)
  - [Looking for help?](#looking-for-help)

## The Speed Wheel

It was 1996 when I bought a Genius Speed Wheel Formula. Back then, I used the DB15 Creative Sound Blaster's port as input for my game pads. It was the common way to connect devices. Few years later, USB took over DB15 as standard for gamepads.

![The speed wheel](./images/01%20speed%20wheel.jpg)

Some months ago I found my old speed wheel laying into a box and I thought that probably I could do something with it. After some thinking and research I decided that the best thing I could do is to use the hardware (mainly the buttons) and adapt the circuits from their analog version to a digital one. First I choose Arduino as the micro controller to use to take control of the new digital input, but few weeks later the Raspberry Pi foundation released the Pico 2040 and I decided to switch my prototype to the Pico because:

- Can be programmed in Python (I'm more skilled in Python than in C)
- Using CircuitPython, the Pico can be seen by the Pc as a GamePad. This is key, since it simplyfies terribly the setup: plug and play :-)

## The new wiring

The speed wheel in mainly 2 potentiometers and 10 buttons:

- A potentiometer to measure the wheel position
- A potentiometer to measure the gear lever position
- 10 Buttons for interacting with the game

![Original circuit](images/02%20original%20circuit.jpg)
![Original circuit](images/03%20original%20circuit.jpg)

My model also includes two gas pedals for breaking and accelerating. For starting, I did not include them, but are easy to integrate since all the wiring is there and it is just 2 more potentiometers.


The DB15 connector does not have cables available for all the buttons: it shares wires for the 2 buttons, changing the current by the means of transistors. With the Pico, and all the digital inputs that it provides, we do not need the transistors anymore.

![Gear lever buttons](images/04%20original%20circuit.jpg)

After looking closely to the circuit, I removed with a solder the transistors and resistors. Fortunately, I only had to add an extra cable for one of the buttons. For the rest, I used the current cables. Keep in mind, that for detecting switches (buttons) in the Pico, we only need a cable that provides current to the switch and another one that connects to the GPIO port.

![Wheel buttons](images/05%20original%20circuit.jpg)

For the connection of the cables to the Pico I reused the previous Dupont connectors. It is important to keep track of what cable (color) goes to which GPIO.

![Connections to the Pico](images/06%20Pico%20connections.jpg)

The part I feel less proud of is the connection of all the Vcc cables (some duct tape), but it works as a charm :-)

![Final result](images/07%20Overview.jpg)

## The code

For the software development I decided to go with VS Code and the [Circuit Python extension](https://marketplace.visualstudio.com/items?itemName=joedevivo.vscode-circuitpython) that simplifies the process of deploying [Circuit Python](https://circuitpython.readthedocs.io/en/latest/docs/index.html) into the [Pico](https://www.raspberrypi.org/products/raspberry-pi-pico/). The setup is simple: USB cable from the Pico to your computer, that is detected as a USB drive. I could develop both in the computer or directly into the Pico.

You can find the current stable version of the software in the [code.py](code.py) file. For using this with your own wheel you **will need to calibrate the values of the potentiometers**. Make use of the `calibrate_analog_input` function to find the maximum and minimum values. You need to change the code with this new values for having the wheel behave correctly.

I'm planning to incorporate a [Kalman filter](https://en.wikipedia.org/wiki/Kalman_filter) for smoothing the wheel and lever output.

Once the code is running in the Pico the wheel is already detected as an input device by the computer. You can install and run [Super TuxKart](https://supertuxkart.net/Main_Page), configure the Speed Wheel as input device, and have fun!

## Looking for help?

Did you get inspired by this post and tried to resurrect your own gamepad? Do not hesitate to clone and modify my code or open an issue to share your thoughts.

Have fun!
