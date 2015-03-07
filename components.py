#!/usr/bin/env python
#
# This file is part of Aquascapi.
# Aquascapi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# Aquascapi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Aquascapi.  If not, see <http://www.gnu.org/licenses/>.
# Copyright Rafael Lopes

import wiringpi2 as wiringpi
import logging
import time


class NotAPinException(Exception):

    """
    Exception raised when trying to use a pin number non existent or None.
    """
    pass


class LightChannel(object):

    """
    Control a led channel with PWM Signal
    Try to use hardware pwm when available.
    """
    PWM_CAPABLE_PINS = [18, 19]

    def __init__(self, pin_number=None):
        super(LightChannel, self).__init__()
        self.pin_number = pin_number
        self.setup()

    def setup(self):
        '''
        Initialize pwm output to zero.
        '''
        if not self.pin_number:
            raise NotAPinException("%s is not a pin", self.pin_number)

        if self.pin_number not in LightChannel.PWM_CAPABLE_PINS:
            wiringpi.softPwmCreate(self.pin_number, 0, 100)

            def change_duty(duty):
                wiringpi.softPwmWrite(self.pin_number, duty)
            self._change_duty_cicle_function = change_duty
        else:
            wiringpi.pinMode(self.pin_number, wiringpi.GPIO.PWM_OUTPUT)

            def change_duty(duty):
                wiringpi.pwmWrite(self.pin_number, int((duty / 100.0) * 1024))
            self._change_duty_cicle_function = change_duty
        self.off()

    def potency(self, percentage=None):
        """
        Set potency to percentage using pwm cycle.
        """
        percentage = max(0, min(percentage, 100))
        self._change_duty_cicle_function(percentage)
        self._duty = percentage
        logging.debug('{} at {}'.format(self.pin_number, self._duty))

    def on(self):
        """
        Set potency to full
        """
        self.potency(100)

    def off(self):
        """
        Set potency to zero
        """
        self.potency(0)


class NormallyOffRelay(object):

    '''
    Controls a relay that always.
    '''

    def __init__(self, pin_number):
        super(NormallyOffRelay, self).__init__()
        self.pin_number = pin_number
        self.setup()

    def setup(self):
        wiringpi.pinMode(self.pin_number, wiringpi.GPIO.OUTPUT)
        wiringpi.digitalWrite(self.pin_number, 0)

    def on(self):
        wiringpi.digitalWrite(self.pin_number, 1)

    def off(self):
        wiringpi.digitalWrite(self.pin_number, 0)


class Solenoid(NormallyOffRelay):

    """
    Controls a relay board to turn to switch between a solenoid and a
    waterpump/oxygen injector.
    """
    pass


class Peristaltic(NormallyOffRelay):

    """
    Controls a relay board to turn to switch between a peristaltic pump.
    """
    DEFAULT_FLOW = 0.5  # default flow of 30ml/minute or 0.5ml/s

    def pump(self, mililiters):
        flow_rate = getattr(self, 'flow_rate', self.DEFAULT_FLOW)
        time_to_pump = mililiters / flow_rate
        self.on()
        time.sleep(time_to_pump)
        self.off()


if __name__ == '__main__':
    wiringpi.wiringPiSetupGpio()
    c1 = LightChannel(18)
    c2 = LightChannel(19)
    c1.on()
    time.sleep(2)
    c2.on()
    time.sleep(2)
    c1.potency(50)
    time.sleep(2)
    c2.potency(50)
    time.sleep(2)
    c2.off()
    c1.off()
    try:
        while True:
            t = 0
            while t < 10:
                c1.potency(50 - (t * 5))
                c2.potency(t * 5)
                t = t + 0.03
                time.sleep(0.03)
            c1, c2 = c2, c1
    except KeyboardInterrupt:
        logging.debug('exit')
    finally:
        c2.off()
        c1.off()
