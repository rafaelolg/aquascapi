import wiringpi2 as wiringpi

class LightChannel(object):
	"""
	Control a led channel with PWM Signal
	Try to use hardware pwm when available.
	"""
	PWM_CAPABLE_PINS = [18,]
	def __init__(self, pin_number):
		super(LightChannel, self).__init__()
		self.pin_number = pin_number

	def setup():
		'''
		Initialize pwm output to zero. 
		'''
		if self.pin_number not in PWM_CAPABLE_PINS:
			wiringpi.softPwmCreate(self.pin_number,0, 100)
			def change_duty(self, duty):
				wiringpi.softPwmWrite(self.pin_number, duty)
			self._change_duty_cicle_function =  change_duty
		else:
			wiringpi.pinMode(self.pin_number, wiringpi.GPIO.PWM_OUTPUT)
			def change_duty(self, duty):
				wiringpi.pwmWrite(self.pin_number, (duty/100.0) * 1024)
			self._change_duty_cicle_function =  change_duty
		self.off()

	def potency(self, percentage=None):
		if percentage:
			percentage = max(0, min(percentage, 100))
			self._change_duty_cicle_function(percentage)
			self._duty = percentage
		else:
			return self._duty

	def on(self):
		self.potency(0)
	
	def off(self):
		self.potency(100)


if __name__ == '__main__':
	import wiringpi2 as wiringpi  
	wiringPiSetupPhys()
	import time
	l_17 = LightChannel(17)
	l_18 = LightChannel(18)
	l_17.on()
	time.sleep(2)
	l_18.on()
	time.sleep(2)
	l_17.potency(50)
	time.sleep(2)
	l_18.potency(50)
	time.sleep(2)
	l_18.off()
	l_17.off()
	
	