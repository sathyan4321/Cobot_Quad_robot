import machine
import utime

class Ultrasonic:
	def __init__(self):
		self.trigger = machine.Pin(16, machine.Pin.OUT)
		self.echo = machine.Pin(17, machine.Pin.IN)

	def distance(self):
		utime.sleep(0.5)
		self.trigger.off()
		utime.sleep_us(3)
		self.trigger.on()
		utime.sleep_us(4)
		self.trigger.off()

		start = utime.ticks_us()

		while self.echo.value() == 0:
			if utime.ticks_diff(utime.ticks_us(), start) > 30000:
				return None
		sent_time = utime.ticks_us()

		while self.echo.value() == 1:
			if utime.ticks_diff(utime.ticks_us(), sent_time) > 30000:
				return None
		received_time = utime.ticks_us()

		duration = utime.ticks_diff(received_time, sent_time)
		distance = (duration * 0.0343) / 2

		return distance





