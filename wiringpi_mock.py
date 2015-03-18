import logging

def digitalWrite(pin_number, value):
    logging.debug('digitalWrite %s, %s', pin_number, value)

def pinMode(pin_number, value):
    logging.debug('pinMode %s, %s', pin_number, value)

def pwmWrite(pin_number, value):
    logging.debug('pwmWrite %s, %s', pin_number, value)

def softPwmWrite(pin_number, duty):
    logging.debug('softPwmWrite %s, %s', pin_number, duty)

def wiringPiSetupGpio():
    logging.debug('wiringPiSetupGpio')

class Mock(object):
	PWM_OUTPUT="GPIO.PWM_OUTPUT"
	OUTPUT="OUTPUT"

GPIO = Mock()