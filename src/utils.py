import time
from SCSCtrl import TTLServo
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import cosine
from torchvision import models, transforms
import torch


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

    
def is_floor(image, model, device, floor_prototype):
    # Przekształcenie fragmentu na embedding
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    fragment_tensor = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        embedding = model(fragment_tensor).cpu().numpy().flatten()
        distance = cosine(embedding, floor_prototype)

    return distance

# Funkcja sprawdzająca, czy przed robotem jest czerwony piksel (przeszkoda)
def any_red_20_20(map_grid, robot_direction, robot_x, robot_y):
    for dx in range(-10, 10):
        for dy in range(0, 20):  # Robot widzi tylko do przodu
            angle_rad = np.radians(robot_direction)
            x_offset = int(dx * np.cos(angle_rad) - dy * np.sin(angle_rad))
            y_offset = int(dx * np.sin(angle_rad) + dy * np.cos(angle_rad))

            cell_x = robot_x + x_offset
            cell_y = robot_y + y_offset

            if map_grid[cell_x, cell_y] == 5:  # Przeszkoda wykryta
                return True  # Przed robotem jest przeszkoda
    return False
                
def move_forward(robot, speed):
    """
    Porusza robotem do przodu.
    """
    robot.left_motor.value = speed
    robot.right_motor.value = speed

def stop(robot):
    """
    Zatrzymuje robota.
    """
    robot.left_motor.value = 0
    robot.right_motor.value = 0
    
def turn_by_angle(robot, angle, turn_speed=0.2):
    """
    Obraca robota o określony kąt, uwzględniając prędkość obrotu.
    :param robot: Obiekt robota.
    :param angle: Kąt w stopniach (dodatni = w prawo, ujemny = w lewo).
    :param turn_speed: Prędkość obrotu (zakres od 0.1 do 1.0).
    """
    # Bazowy czas obrotu o 90° dla TURN_SPEED=0.2
    base_turn_speed = 0.2
    base_time_90 = 7.02  # czas obrotu o 90° przy prędkości 0.2

    # Oblicz czas obrotu dla 90° przy zadanej prędkości
    turn_time_90 = base_time_90 * (base_turn_speed / turn_speed)

    # Oblicz czas obrotu dla zadanego kąta
    abs_angle = abs(angle)
    turn_time = turn_time_90 * (abs_angle / 90)

    # Kierunek obrotu
    if angle > 0:  # Obrót w prawo
        robot.left_motor.value = turn_speed
        robot.right_motor.value = -turn_speed
    else:  # Obrót w lewo
        robot.left_motor.value = -turn_speed
        robot.right_motor.value = turn_speed

    # Obrót przez określony czas
    time.sleep(turn_time)
    robot.left_motor.value = 0
    robot.right_motor.value = 0
    #print(f"Obrót o {angle}° zakończony w czasie {turn_time:.2f} sekundy (prędkość: {turn_speed}).")

