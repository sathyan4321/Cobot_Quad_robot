# Run on the Pico: each leg swings FORWARD, then back to centre, one at a time.
# Watch which way each leg really moves, then fix DIR in robot_movement.py.
from robot_movement import move
import utime
m = move()
m.stand()
utime.sleep(1)
for leg in ("fl", "fr", "bl", "br"):
    print("Leg", leg, "-> should swing FORWARD now")
    m._glide({leg: 30})
    utime.sleep(1)
    m._glide({leg: 0})
    utime.sleep(0.5)
m.stand()
