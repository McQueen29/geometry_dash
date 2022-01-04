import pygame as pg
import sys
import pygame
import os

pygame.init()
screen = pygame.display.set_mode((800, 800))
tile_width = tile_height = 50
all_sprites = pygame.sprite.Group()
blocks_group = pygame.sprite.Group()
air_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f'Файл с озображением {fullname} отсутствует')
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is None:
        image = image.convert_alpha()
    else:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image

player_image = load_image('Player.png')
player_image = pygame.transform.scale(player_image, (50, 50))
box_images = load_image('box.png')
air_image = load_image('grass.png')


def load_skin():
    pass


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    text = ["Заставка", "",
            "Правила игры", "Если в правилах несколько строк,", ""
            "то приходится выводить их построчно"]
    fon = pygame.transform.scale(load_image('fon.jpg'), (800, 400))
    screen.fill(pygame.Color('blue'))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for el in text:
        rendered_line = font.render(el, 1, pygame.Color(200, 255, 200))
        intro_rect = rendered_line.get_rect()
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height + 10
        screen.blit(rendered_line, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(50)


def load_level(filename):
    filename = 'levels/' + filename
    with open(filename, 'r', encoding='utf-8') as mapfile:
        level_map = [line.strip() for line in mapfile.readlines()]
    max_width = max([len(x) for x in level_map])
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Blocks('wall', x, y)
            elif level[y][x] == '@':
                new_player = DefaultPlayer(x, y)
    return new_player, x, y


class Blocks(pg.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(blocks_group, all_sprites)
        self.image = box_images
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y)


class Air(pg.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(air_group, all_sprites)
        self.image = air_image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y)


class DefaultPlayer(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x + 15, tile_height * pos_y + 5)

    def update(self, key=None):
        self.rect.x += 10


class SmallPlayer(pg.sprite.Sprite):
    pass


class FlyingPlayer(pg.sprite.Sprite):
    pass


class FlyingPortal(pg.sprite.Sprite):
    pass


class InvertedPortal(pg.sprite.Sprite):
    pass


class SmallPortal(pg.sprite.Sprite):
    pass


class Jumper(pg.sprite.Sprite):
    pass


class InverterPoint(pg.sprite.Sprite):
    pass


class JumpPoint(pg.sprite.Sprite):
    pass


class Coin(pg.sprite.Sprite):
    pass


class Statistics():
    pass


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = width // 2 - target.rect.x - target.rect.w // 2
        self.dy = height // 2 - target.rect.y - target.rect.h // 2


def draw_screen():
    pass


if __name__ == '__main__':
    width = 800
    height = 800
    running = True
    camera = Camera()
    clock = pygame.time.Clock()
    start_screen()
    player, level_x, level_y = generate_level(load_level('first'))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        player_group.update()
        screen.fill(pygame.Color('black'))
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        blocks_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()