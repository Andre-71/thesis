from djitellopy import tello

drone =  tello.Tello()
drone.connect()

drone.connect_to_wifi(ssid="2771", password="Vladilena")
