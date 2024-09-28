#!/usr/bin/env python3

import logging
import sys
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, MediumMotor
from ev3dev2.motor import MoveTank
from ev3dev2.control.rc_tank import RemoteControlledTank
from ev3dev2.sensor.lego import ColorSensor
from time import sleep
from ev3dev2.sound import Sound

class RemoteControlledTank(MoveTank):
    def __init__(self, left_motor_port, right_motor_port, polarity='inversed', speed=400, channel=1):
        MoveTank.__init__(self, left_motor_port, right_motor_port)
        self.set_polarity(polarity)

        left_motor = self.motors[left_motor_port]
        right_motor = self.motors[right_motor_port]
        self.speed_sp = speed
        logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s %(levelname)5s %(filename)s:%(lineno)5s - %(funcName)25s(): %(message)s")
        log = logging.getLogger(__name__)
        log.info("Starting EV3D4")

        logging.addLevelName(logging.ERROR, "\033[91m  %s\033[0m" % logging.getLevelName(logging.ERROR))
        logging.addLevelName(logging.WARNING, "\033[91m%s\033[0m" % logging.getLevelName(logging.WARNING))
        color_sensor = ColorSensor()
        
        while(True):
            color_sensor.calibrate_white
            color = color_sensor.color
            colorRgb = color_sensor.rgb

            r = colorRgb[0]
            g = colorRgb[1]
            b = colorRgb[2]

            text = ColorSensor.COLORS[color]
            log.info(text)
            log.info(colorRgb)

            log.info(r)
            log.info(g)
            log.info(b)

            if(g > 10):
                self.make_move(one=True, two=left_motor, three=self.speed_sp)
                self.make_move(one=True, two=right_motor, three=self.speed_sp)

            if(g < 10):
                self.make_move(one=False, two=left_motor, three=self.speed_sp)
                self.make_move(one=False, two=right_motor, three=self.speed_sp)

    def make_move(self, one, two, three):
        if one:
            two.run_forever(speed_sp=three)
        else:
            two.stop()

    # def main(self):

    #     try:
    #         while True:
    #             self.remote.process()
    #             sleep(0.01)

    #     # Exit cleanly so that all motors are stopped
    #     except (KeyboardInterrupt, Exception) as e:
    #         log.exception(e)
    #         self.off()

class EV3D4RemoteControlled(RemoteControlledTank):

    def __init__(self, medium_motor=OUTPUT_A, left_motor=OUTPUT_C, right_motor=OUTPUT_B):
        RemoteControlledTank.__init__(self, left_motor, right_motor)
        self.medium_motor = MediumMotor(medium_motor)
        self.medium_motor.reset()


if __name__ == '__main__':
    ev3d4 = EV3D4RemoteControlled()
    ev3d4.main()




