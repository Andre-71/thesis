from djitellopy import tello
import cv2

drone =  tello.Tello()
drone.connect(wait_for_state=False)
drone.streamon()
counter = 1

while True:
    if counter == 1000000:
        break
    img = drone.get_frame_read().frame
    if img is not None:
        img = cv2.resize(img, (360, 240))
        cv2.imshow("Image", img)
        cv2.waitKey(1)
    counter += 1

drone.streamoff()
drone.end()