import traitlets
import numpy as np
from jetbot import bgr8_to_jpeg

class MapProvider(traitlets.HasTraits):
    value = traitlets.Bytes()

    def __init__(self, map_size):
        super().__init__()
        self.map_size = map_size
        # Poniżej przykładowe inicjalne wartości (możesz podmienić na swoje)
        self.robot_x = map_size / 2
        self.robot_y = map_size / 2
        self.map_grid = np.zeros((self.map_size, self.map_size), dtype=int)
        self.lut = np.array([
            [169, 169, 169],  # index 0 => dla map_grid == -1
            [0,   255, 0],    # index 1 => dla map_grid ==  0
            [255, 200, 50],  # index 2 => dla map_grid ==  1
            [255, 165, 20],   # index 3 => dla map_grid ==  2
            [255, 140, 0],    # index 4 => dla map_grid ==  3
            [255, 100, 0],    # index 5 => dla map_grid ==  4
            [255, 0,   0],    # index 6 => dla map_grid ==  5
        ], dtype=np.uint8)
        
        # Tworzymy początkowy obraz (wartości w self.value)
        self.update_map()
        
    def _draw_robot(self, img, radius=6, color=(255, 0, 0)):
        height, width, _ = img.shape
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                # obliczamy odległość euklidesową od środka
                if dx*dx + dy*dy <= radius*radius:
                    px = int(self.robot_x) + dx
                    py = int(self.robot_y) + dy
                    # sprawdzamy, czy punkt mieści się w granicach obrazka
                    if 0 <= px < width and 0 <= py < height:
                        img[py, px] = color

    def update_map(self):
        # 1) Obliczamy indeksy do tablicy LUT
        indices = self.map_grid + 1  # -1 -> 0, 0 -> 1, ..., 5 -> 6
        # 2) Pobieramy kolory w trybie wektorowym
        img = self.lut[indices]      # shape => (map_size, map_size, 3)
        # 3) Rysujemy pozycję robota (bez OpenCV)
        self._draw_robot(img)
        # 4) Odwracamy pionowo, jeśli chcesz mieć (0,0) na dole
        img = np.flipud(img)
        # 5) Kodujemy do JPEG
        self.value = bgr8_to_jpeg(img)

    def set_map(self, map_grid):
        self.map_grid = map_grid
        self.update_map()
    
    def set_robot_pos(self, x, y):
        self.robot_x = x
        self.robot_y = y
        self.update_map()
        
    def update_map_grid(self, detection, robot_x, robot_y, robot_direction, map_grid):
        angle_rad = np.radians(robot_direction)

        for dx in range(-10, 10):   # dx = lewo/prawo
            for dy in range(0, 20): # dy = przód/tył
                # Transformacja (lx, ly) -> (global_x, global_y)
                #  tu: 0° => jedź w górę = rosnące global_y

                x_offset = int(dx * np.cos(angle_rad) - dy * np.sin(angle_rad))
                y_offset = int(dx * np.sin(angle_rad) + dy * np.cos(angle_rad))

                # W map_grid:  map_grid[row=y, col=x]
                cell_x = int(robot_x + x_offset)
                cell_y = int(robot_y + y_offset)

                # Uwaga: zapisy do map_grid[y, x] => map_grid[cell_y, cell_x]
                if detection < 0.175:
                    map_grid[cell_y, cell_x] = 0
                elif 0.175 <= detection < 2.05:
                    if 1 <= map_grid[cell_y, cell_x] < 4:
                        map_grid[cell_y, cell_x] += 1
                    elif map_grid[cell_y, cell_x] == -1:
                        map_grid[cell_y, cell_x] = 1
                else:
                    map_grid[cell_y, cell_x] = 5
