import logging


class GPIOObject(object):
    PWM_OUTPUT = 2
    OUTPUT = 1


class WirinpiWrapper(object):
    """Wrapper for wiringpi2"""
    def __init__(self, mocking=False):
        self.mocking = mocking
        self.GPIO = GPIOObject()

    def digitalWrite(self, pin_number, value):
        logging.debug('digitalWrite %s, %s', pin_number, value)
        if not self.mocking:
            import wiringpi2
            wiringpi2.digitalWrite(pin_number, value)

    def pinMode(self, pin_number, value):
        logging.debug('pinMode %s, %s', pin_number, value)
        if not self.mocking:
            import wiringpi2
            wiringpi2.pinMode(pin_number, value)

    def pwmWrite(self, pin_number, value):
        logging.debug('pwmWrite %s, %s', pin_number, value)
        if not self.mocking:
            import wiringpi2
            wiringpi2.pwmWrite(pin_number, value)

    def softPwmWrite(self, pin_number, duty):
        logging.debug('softPwmWrite %s, %s', pin_number, duty)
        if not self.mocking:
            import wiringpi2
            wiringpi2.softPwmWrite(pin_number, duty)

    def wiringPiSetupGpio(self):
        logging.debug('wiringPiSetupGpio')
        if not self.mocking:
            import wiringpi2
            wiringpi2.wiringPiSetupGpio()

    def delay(self, milliseconds):
        logging.debug('delay')
        if not self.mocking:
            import wiringpi2
            wiringpi2.delay(milliseconds)

