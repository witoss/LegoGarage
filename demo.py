from time import sleep
from ev3dev.ev3 import *

# Connect two large motors on output ports B and C
lmotor = LargeMotor('outB')
rmotor = LargeMotor('outC')
mmotor = MediumMotor('outA')

# Connect remote control
rc = RemoteControl()

# Initialize button handler
# button = Button()   # not working so disabled

# Turn leds off t
Leds.all_off()

def roll(motor, led_group, direction):
    """
    Generate remote control event handler. It rolls given motor into given
    direction (1 for forward, -1 for backward). When motor rolls forward, the
    given led group flashes green, when backward -- red. When motor stops, the
    leds are turned off.

    The on_press function has signature required by RemoteControl class.
    It takes boolean state parameter; True when button is pressed, False
    otherwise.
    """
    def on_press(state):
        if state:
            # Roll when button is pressed
            motor.run_forever(speed_sp=1000*direction)
            Leds.set_color(led_group, direction > 0 and Leds.GREEN or Leds.RED)
        else:
            # Stop otherwise
            motor.stop(stop_action='brake')
            Leds.set(led_group, brightness_pct=0)

    return on_press

# Assign event handler to each of the remote buttons
rc.on_red_up    = roll(lmotor, Leds.LEFT,   1)
rc.on_red_down  = roll(lmotor, Leds.LEFT,  -1)
rc.on_blue_up   = roll(rmotor, Leds.RIGHT,  1)
rc.on_blue_down = roll(rmotor, Leds.RIGHT, -1)
rc.on_beacon = roll(mmotor, Leds.RIGHT, -1)

# Enter event processing loop
#while not button.any():   #not working so commented out
while True:   #replaces previous line so use Ctrl-C to exit
    rc.process()
    sleep(0.01)
