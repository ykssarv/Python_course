"""Robot."""
from PiBot import PiBot
robot = PiBot()
fast = 12
slow = 4
robot.set_wheels_speed(5)
while True:
    robot.sleep(0.1)
    if sum(robot.get_right_line_sensors()) > 2400 and sum(robot.get_left_line_sensors()) > 2400:
        break
    if sum(robot.get_left_line_sensors()) > sum(robot.get_right_line_sensors()):
        robot.set_left_wheel_speed(fast)
        robot.set_right_wheel_speed(slow)
    elif sum(robot.get_left_line_sensors()) < sum(robot.get_right_line_sensors()):
        robot.set_left_wheel_speed(slow)
        robot.set_right_wheel_speed(fast)
    else:
        robot.set_wheels_speed(fast)
robot.set_wheels_speed(0)
robot.done()
