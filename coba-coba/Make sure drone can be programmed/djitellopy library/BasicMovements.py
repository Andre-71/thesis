from djitellopy import tello
from time import sleep

drone =  tello.Tello()
drone.connect()

drone.takeoff()

# drone.send_rc_control(0, 50, 0, 0)
sleep(0.5)
drone.flip_left()
sleep(0.5)
# drone.send_rc_control(0, 0, 0, 0)

drone.land()
drone.end()