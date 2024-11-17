import pygame
import sys
import random
# Initialize Pygame
pygame.init()

# Player settings
player_size = 50
player_color = (0, 128, 255)
player_speed = 5

# Map settings
tile_size = 50
map_width = 20  # Number of tiles wide
map_height = 20  # Number of tiles high

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((player_size, player_size))
        self.image.fill(player_color)
        self.rect = self.image.get_rect()
        self.rect.center = (map_width * tile_size // 2, map_height * tile_size // 2)  # Start in the center of the map

    def update(self, keys_pressed):
        if keys_pressed[pygame.K_LEFT]:
            self.rect.x -= player_speed
        if keys_pressed[pygame.K_RIGHT]:
            self.rect.x += player_speed
        if keys_pressed[pygame.K_UP]:
            self.rect.y -= player_speed
        if keys_pressed[pygame.K_DOWN]:
            self.rect.y += player_speed

# Camera class
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(self.width / 2)
        y = -target.rect.centery + int(self.height / 2)

        # Limit scrolling to map size
        x = min(0, x)  # Left
        y = min(0, y)  # Top
        x = max(-(map_width * tile_size - self.width), x)  # Right
        y = max(-(map_height * tile_size - self.height), y)  # Bottom

        self.camera = pygame.Rect(x, y, self.width, self.height)

# Map class
class Map:
    def __init__(self, width, height, tile_size):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.map_data = self.generate_mapv2()

    def generate_map(self):
        # Generate a simple map with a border and some objects
        map_data = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
                    row.append(1)  # Border tile
                elif (x + y) % 5 == 0:  # Add some objects
                    row.append(2)  # Object tile
                else:
                    row.append(0)  # Empty tile
            map_data.append(row)
        return map_data
    
    def generate_mapv2(self):
        map_matrix = []

        min_h = 0
        max_h = 2

        matrix_height = self.height
        matrix_width = self.width
        step = 0.2

        for i in range(matrix_height):
            layer = []
            for j in range(matrix_width):
                layer.append(random.randint(min_h, max_h))
            map_matrix.append(layer)
        return map_matrix

    def draw(self, screen, camera):
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                rect = pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                if tile == 1:
                    color = (255, 255, 0)  # Border tile color
                elif tile == 2:
                    color = (0, 255, 0)  # Object tile color
                elif tile == 0:
                    color = (0, 0, 255)
                else:
                    continue
                pygame.draw.rect(screen, color, camera.apply(rect))

# Game class
class Game:
    def __init__(self):
        self.width = 500
        self.height = 500
        self.flags = pygame.RESIZABLE
        self.screen = pygame.display.set_mode((self.width, self.height), self.flags)
        self.running = True
        self.background_color = (0, 0, 0)

        self.player = Player()
        self.camera = Camera(self.width, self.height)
        self.map = Map(map_width, map_height, tile_size)

        self.__update()

    def __eventHandler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def __draw(self):
        self.map.draw(self.screen, self.camera)
        self.screen.blit(self.player.image, self.camera.apply(self.player.rect))

    def __update(self):
        clock = pygame.time.Clock()
        while self.running:
            self.__eventHandler()
            keys_pressed = pygame.key.get_pressed()
            self.player.update(keys_pressed)
            self.camera.update(self.player)
            self.screen.fill(self.background_color)
            self.__draw()
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()

# Create and run the game
game = Game()
