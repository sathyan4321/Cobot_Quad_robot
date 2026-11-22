import servo
import utime

class move:
	# ---- Gait tuning (edit these, not the code) ----
	# +1 means "angle goes DOWN to swing the leg forward" (0 = forward),
	# -1 means "angle goes UP to swing the leg forward" (180 = forward).
	# If the robot ROTATES, one side is inverted: flip the sign of that side.
	DIR   = {"fl": 1, "fr": -1, "bl": 1, "br": -1}
	TRIM  = {"fl": 0, "fr": 0, "bl": 0, "br": 0}   # per-leg centre offset (deg)
	STRIDE = 25      # swing amount from vertical (deg); bigger = longer step
	STEPS = 12       # interpolation steps per half-cycle (smoother = less slip)
	STEP_MS = 20     # ms per interpolation step

	def __init__(self):
		self.pos = {"fl": 90, "fr": 90, "bl": 90, "br": 90}
		self.fl = servo.Servo(0) #0 - forward 
		self.fr = servo.Servo(1) #180 - forward
		self.bl = servo.Servo(2) #0 - forward
		self.br = servo.Servo(3) #180 - forward


	def stand(self):
		self.fl.angle(90)
		self.fr.angle(90)
		self.bl.angle(90)
		self.br.angle(90)
		print("Stand")
		
		
	def sit(self):
		self.fl.angle(0)
		self.fr.angle(180)
		self.bl.angle(180)
		self.br.angle(0)
		print("Sit")
		
		
	def hello(self):
		self.stand()
		print("hello")
		utime.sleep(0.4)
		for i in range(3):
			self.fl.angle(0)
			utime.sleep(0.3)
			self.fl.angle(80)
			utime.sleep(0.3)
		self.stand()

	def ready(self):
		self.fl.angle(80)
		self.fr.angle(100)
		self.bl.angle(100)
		self.br.angle(80)
		print("Ready")

	def play(self):
		self.fl.angle(10)
		self.fr.angle(170)
		self.bl.angle(90)
		self.br.angle(90)
		print("Play")

	def _target(self, leg, offset):
		# offset > 0 = leg swung forward, < 0 = swung backward
		return 90 + self.TRIM[leg] - self.DIR[leg] * offset

	def _glide(self, offsets):
		# Move all legs together to the target offsets in small steps
		legs = {"fl": self.fl, "fr": self.fr, "bl": self.bl, "br": self.br}
		start = dict(self.pos)
		end = {l: self._target(l, o) for l, o in offsets.items()}
		for i in range(1, self.STEPS + 1):
			for l in end:
				a = start[l] + (end[l] - start[l]) * i / self.STEPS
				legs[l].angle(a)
				self.pos[l] = a
			utime.sleep_ms(self.STEP_MS)

	def forward(self):
		# Diagonal gait: fl+br swing forward while fr+bl push back, then swap.
		s = self.STRIDE
		self._glide({"fl": s, "br": s, "fr": -s, "bl": -s})
		self._glide({"fl": -s, "br": -s, "fr": s, "bl": s})
		print("Forward")

	def stop(self):
		self.fl.angle(0)
		self.fr.angle(0)
		self.bl.angle(0)
		self.br.angle(0)
		print("Stop")




