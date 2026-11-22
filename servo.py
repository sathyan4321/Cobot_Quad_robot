import machine
import utime

class Servo:
	def __init__(self,pin):
		self.servo = machine.PWM(machine.Pin(pin))
		self.servo.freq(50)


	def angle(self,degree):
		duty = int(500000+((degree/180)*2000000))
		self.servo.duty_ns(duty)
