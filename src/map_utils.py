import traitlets
import numpy as np
from jetbot import bgr8_to_jpeg

class MapProvider(traitlets.HasTraits):
    """
    English: A class that provides a map image in JPEG bytes form as a trait
    that can be linked to a Jupyter widgets.Image.
    
    Polski: Klasa zapewniająca obraz mapy (w bajtach JPEG) jako trait
    (wartość cechy traitlets), którą można połączyć (link) z widgets.Image.
    """
    value = traitlets.Bytes()

    def __init__(self, map_size):
        super().__init__()
        self.map_size = map_size
        # Poniżej przykładowe inicjalne wartości (możesz podmienić na swoje)
        self.robot_x = map_size / 2
        self.robot_y = map_size / 2
        self.map_grid = np.zeros((self.map_size, self.map_size), dtype=int)
        self._color_map = {
            -1: [169, 169, 169],  # Szary - nieznane
             0: [0, 255, 0],      # Zielony - podłoga
             1: [255, 250, 205],  # Bardzo jasnożółty
             2: [255, 215, 0],    # Żółty
             3: [255, 165, 0],    # Pomarańczowy
             4: [255, 140, 0],    # Ciemnopomarańczowy
             5: [255, 0, 0]       # Czerwony - przeszkoda
        }
        
        # Tworzymy początkowy obraz (wartości w self.value)
        self.update_map()
        
    def _draw_robot_circle(self, img, radius=3, color=(255, 0, 0)):
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
        """
        English: Updates the self.value Bytes trait with a new JPEG image
        created from the current map_grid and robot position.
        
        Polski: Aktualizuje atrybut self.value (typ Bytes) nowym obrazem JPEG
        wygenerowanym z obecnej siatki mapy (map_grid) i pozycji robota.
        """
        # Tworzymy pustą tablicę (BGR8)
        img = np.zeros((self.map_size, self.map_size, 3), dtype=np.uint8)
        # Uzupełniamy ją kolorami w zależności od map_grid
        for y in range(self.map_size):
            for x in range(self.map_size):
                value = self.map_grid[x, y]
                img[y, x] = self._color_map.get(value)
        self._draw_robot_circle(img)
        img = np.flipud(img)
        # Kodujemy do JPEG i zapisujemy do self.value
        self.value = bgr8_to_jpeg(img)

    def set_map(self, map_grid):
        """
        English: Set a new map grid and update the displayed image.
        Polski: Ustawia nową siatkę mapy i aktualizuje wyświetlany obraz.
        """
        self.map_grid = map_grid
        self.update_map()
    
    def set_robot_pos(self, x, y):
        """
        English: Set a new robot position (x,y) and update the displayed image.
        Polski: Ustawia nową pozycję robota (x,y) i aktualizuje wyświetlany obraz.
        """
        self.robot_x = y
        self.robot_y = x
        self.update_map()
