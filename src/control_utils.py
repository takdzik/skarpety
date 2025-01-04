from SCSCtrl import TTLServo

def resetCameraPosition():
    # Dodanie korekty
    servoPos_1 = -2  # Skorygowanie pan (prawo-lewo)
    servoPos_5 = 0   # Tilt bez korekty

    TTLServo.servoAngleCtrl(1, servoPos_1, 1, 150)
    TTLServo.servoAngleCtrl(5, servoPos_5, 1, 150)
