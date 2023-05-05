"""Robot."""
from PiBot import PiBot

robot = PiBot()

robot.set_wheels_speed(5)
while True:
    robot.sleep(0.1)
    if robot.get_leftmost_line_sensor() < 200:
        break
robot.sleep(4)
robot.set_wheels_speed(0)
robot.done()
