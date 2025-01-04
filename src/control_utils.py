import time
from SCSCtrl import TTLServo


def resetCameraPosition():
    # Dodanie korekty
    servoPos_1 = -2  # Skorygowanie pan (prawo-lewo)
    servoPos_5 = 0   # Tilt bez korekty

    TTLServo.servoAngleCtrl(1, servoPos_1, 1, 150)
    TTLServo.servoAngleCtrl(5, servoPos_5, 1, 150)
    
def forward_with_correction(robot, speed=0.5, correction=0.0, duration=None):
    """
    Jedzie do przodu z korekcją prędkości dla jednego z silników.
    
    :param robot: Obiekt robota.
    :param speed: Prędkość podstawowa (0.0 do 1.0).
    :param correction: Korekta prędkości dla prawego silnika (-1.0 do 1.0).
    :param duration: Czas jazdy (jeśli None, działa do zatrzymania).
    """
    left_speed = speed
    right_speed = speed + correction
    robot.set_motors(left_speed, right_speed)
    
    if duration:
        time.sleep(duration)
        robot.stop()
        
def measure_speed_with_correction(robot, distance_meters, speed=0.5, correction=0.0):
    """
    Mierzy prędkość robota z uwzględnieniem korekcji prędkości silników.
    
    :param robot: Obiekt robota.
    :param distance_meters: Dystans do pokonania w metrach.
    :param speed: Prędkość podstawowa (0.0 do 1.0).
    :param correction: Korekta prędkości dla prawego silnika (-1.0 do 1.0).
    :return: Zmierzona prędkość w m/s.
    """
    print(f"Rozpoczynam pomiar na dystansie {distance_meters} m...")
    
    # Ustawienie prędkości silników
    left_speed = speed
    right_speed = speed + correction
    robot.set_motors(left_speed, right_speed)
    
    # Rozpoczęcie pomiaru czasu
    start_time = time.time()
    
    # Czekamy na zakończenie przejazdu
    input("Naciśnij ENTER, gdy robot osiągnie cel...")
    
    # Zatrzymanie robota
    robot.stop()
    
    # Obliczenie czasu przejazdu
    elapsed_time = time.time() - start_time
    print(f"Czas przejazdu: {elapsed_time:.2f} sekund")
    
    # Obliczenie prędkości
    measured_speed = distance_meters / elapsed_time
    print(f"Zmierzona prędkość: {measured_speed:.2f} m/s")
    return measured_speed

