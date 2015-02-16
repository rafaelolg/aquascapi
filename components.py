import wiringpi2 as wiringpi
import logging


class LightChannel(object):

    """
    Control a led channel with PWM Signal
    Try to use hardware pwm when available.
    """
    PWM_CAPABLE_PINS = [18, 19]

    def __init__(self, pin_number):
        super(LightChannel, self).__init__()
        self.pin_number = pin_number
        self.setup()

    def setup(self):
        '''
        Initialize pwm output to zero.
        '''
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
        percentage = max(0, min(percentage, 100))
        self._change_duty_cicle_function(percentage)
        self._duty = percentage
        logging.debug('{} at {}'.format(self.pin_number, self._duty))

    def on(self):
        self.potency(100)

    def off(self):
        self.potency(0)


class Solenoid(object):

    """
    Controls a relay board to turn to switch between a solenoid and a
    waterpump/oxygen injector.
    """

    def __init__(self, pin_number):
        super(Solenoid, self).__init__()
        self.pin_number = pin_number
        self.setup()

    def setup(self):
        wiringpi.pinMode(self.pin_number, wiringpi.GPIO.OUTPUT)
        wiringpi.digitalWrite(self.pin_number, 0)

    def on(self):
        wiringpi.digitalWrite(self.pin_number, 1)

    def off(self):
        wiringpi.digitalWrite(self.pin_number, 0)


if __name__ == '__main__':
    wiringpi.wiringPiSetupGpio()
    import time
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
    t = 0
    while t < 5:
        c1.potency(50 - (t * 10))
        c2.potency(t * 10)
        t = t + 0.03
        time.sleep(0.03)
    c2.off()
    c1.off()
