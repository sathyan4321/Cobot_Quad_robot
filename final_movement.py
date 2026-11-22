from robot_movement import move
import utime
import ultrasonic
import buzzer

sensor = ultrasonic.Ultrasonic()
move = move()
sound = buzzer.Buzzer(5)

try:
	while True:
		distance = sensor.distance()

		if distance is None:
			print("No object detected")
		elif distance>60:
			print(f"{distance:.2f} cm")
			for i in range(4):
				move.forward()
				utime.sleep(1)
				print(f"{distance:.2f} cm")
			utime.sleep(0.5)
		elif distance>40:
			print(f"{distance:.2f} cm")
			move.stand()
			sound.bark()
			utime.sleep(0.7)
			print(f"{distance:.2f} cm")
		elif distance>30:
			move.stand()
			utime.sleep(0.5)
			move.sit()
			sound.yelp()
			utime.sleep(0.5)
			print(f"{distance:.2f} cm")
		elif distance>20:
			move.stand()
			utime.sleep(0.5)
			move.hello()
			sound.pant()
			utime.sleep(0.5)
			print(f"{distance:.2f} cm")
		elif distance>10:
			move.stand()
			sound.howl()
			utime.sleep(0.5)
			move.play()
			print(f"{distance:.2f} cm")
			utime.sleep(0.7)
		else:
			move.stop()
			print("Robot Stopped")
			sound.whine()
			print(f"{distance:.2f} cm")
			utime.sleep(0.7)

except Exception as e:
	print("Error ", e)