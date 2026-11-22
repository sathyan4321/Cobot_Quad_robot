from machine import Pin, PWM
import time
import math
import random

class Buzzer:
    def __init__(self, pin):
        self.buzzer = PWM(Pin(pin))

    def stop(self):
        self.buzzer.duty_u16(0)

    def _envelope_sweep(self, start_freq, end_freq, duration_ms,
                        peak_duty=40000, attack=0.15, decay=0.25,
                        steps=60, vibrato=0, stutter=False):
        """
        Sweep with a full ADSR-style amplitude envelope.
        attack  = fraction of steps for duty ramp-up
        decay   = fraction of steps for duty fade-out
        stutter = rapidly jitter duty to simulate roughness
        """
        step_ms = duration_ms / steps / 1000
        attack_steps = int(steps * attack)
        decay_start  = steps - int(steps * decay)

        for i in range(steps):
            t = i / steps
            freq = int(start_freq + (end_freq - start_freq) * t)

            if vibrato:
                freq += int(vibrato * math.sin(i * 1.2))
            freq = max(50, freq)

            # Amplitude envelope
            if i < attack_steps:
                duty = int(peak_duty * (i / attack_steps))
            elif i > decay_start:
                fade = (i - decay_start) / (steps - decay_start)
                duty = int(peak_duty * (1 - fade))
            else:
                duty = peak_duty

            # Stutter: random micro-jitter on duty for roughness
            if stutter:
                jitter = random.randint(-5000, 5000)
                duty = max(8000, min(65000, duty + jitter))

            self.buzzer.freq(freq)
            self.buzzer.duty_u16(duty)
            time.sleep(step_ms)

    def _chirp(self, freq, duty, ms):
        """Short high-duty burst — adds bite/texture between sweeps."""
        self.buzzer.freq(freq)
        self.buzzer.duty_u16(duty)
        time.sleep(ms / 1000)
        self.buzzer.duty_u16(0)

    # ── BARK: sharp attack, staccato, with a chest-thump chirp before each ──
    def bark(self):
        for _ in range(2):
            self._chirp(900, 45000, 18)           # throat click
            self._envelope_sweep(
                700, 1300, 90,
                peak_duty=42000,
                attack=0.10, decay=0.35,           # fast attack, tail off
                steps=30, vibrato=0
            )
            self._envelope_sweep(
                1300, 750, 55,
                peak_duty=28000,
                attack=0.0, decay=0.6,
                steps=20
            )
            self.stop()
            time.sleep(0.09)
        self.stop()

    # ── GROWL: low, rough, sustained with heavy stutter + vibrato ──
    def growl(self):
        # Chest rumble build-up
        self._envelope_sweep(
            160, 280, 500,
            peak_duty=44000,
            attack=0.25, decay=0.05,
            steps=70, vibrato=14, stutter=True
        )
        # Sustained threatening hold
        self._envelope_sweep(
            280, 260, 700,
            peak_duty=46000,
            attack=0.0, decay=0.15,
            steps=80, vibrato=20, stutter=True
        )
        # Release
        self._envelope_sweep(
            260, 180, 300,
            peak_duty=30000,
            attack=0.0, decay=0.7,
            steps=35, vibrato=8, stutter=True
        )
        self.stop()

    # ── WHINE: airy, ascending, soft — envelope fades at top ──
    def whine(self):
        # Breathy start
        self._envelope_sweep(
            650, 1600, 400,
            peak_duty=22000,
            attack=0.30, decay=0.10,
            steps=55, vibrato=30
        )
        # Peak — thin, urgent
        self._envelope_sweep(
            1600, 1900, 250,
            peak_duty=18000,
            attack=0.0, decay=0.50,
            steps=30, vibrato=45
        )
        # Sad little fall
        self._envelope_sweep(
            1900, 1100, 200,
            peak_duty=12000,
            attack=0.0, decay=0.80,
            steps=25, vibrato=20
        )
        self.stop()

    # ── HOWL: four-phase arc — build, peak, quiver, fade ──
    def howl(self):
        # Throat clear chirp
        self._chirp(350, 28000, 60)

        # Rising into the howl
        self._envelope_sweep(
            280, 850, 700,
            peak_duty=38000,
            attack=0.35, decay=0.05,
            steps=65, vibrato=8
        )
        # Peak — full vibrato quiver
        self._envelope_sweep(
            850, 920, 600,
            peak_duty=40000,
            attack=0.0, decay=0.05,
            steps=60, vibrato=35
        )
        # Descending with wobble
        self._envelope_sweep(
            920, 500, 700,
            peak_duty=35000,
            attack=0.0, decay=0.20,
            steps=65, vibrato=22
        )
        # Long mournful tail
        self._envelope_sweep(
            500, 280, 600,
            peak_duty=20000,
            attack=0.0, decay=0.85,
            steps=55, vibrato=10
        )
        self.stop()

    # ── PANT: rhythmic breath bursts with soft attack ──
    def pant(self, count=7):
        for i in range(count):
            # Inhale chirp
            self._chirp(800, 12000, 30)
            time.sleep(0.02)
            # Exhale — slightly lower
            self._envelope_sweep(
                650, 580, 70,
                peak_duty=14000,
                attack=0.3, decay=0.5,
                steps=12
            )
            self.stop()
            time.sleep(0.05)

    # ── YELP: instant high peak, sharp fall, echo ──
    def yelp(self):
        self._chirp(2000, 50000, 12)              # spike
        self._envelope_sweep(
            1900, 380, 160,
            peak_duty=30000,
            attack=0.0, decay=0.55,
            steps=28, vibrato=15
        )
        self.stop()
        time.sleep(0.04)
        # Soft echo yelp
        self._envelope_sweep(
            1200, 300, 120,
            peak_duty=16000,
            attack=0.0, decay=0.80,
            steps=20
        )
        self.stop()


# ── Demo ──
#dog = Buzzer()
##dog.growl();  time.sleep(1.2)
#dog.whine();  time.sleep(1.2)
#dog.howl();   time.sleep(1.5)
#dog.pant();   time.sleep(1.0)
#dog.yelp()
