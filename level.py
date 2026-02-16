from pytmx.util_pygame import load_pygame
from settings import *
from support import tmx_importer
from entities import Player

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()
    
    def draw(self, player_center):
        # centraliza a visão do gato
        self.offset.x = player_center[0] - WINDOW_WIDTH / 2
        self.offset.y = player_center[1] - WINDOW_HEIGHT / 2

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = pygame.transform.scale_by(surf, 4)
        self.rect = self.image.get_frect(topleft = pos)

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.all_sprites = AllSprites()
        # self.collision_sprites = pygame.sprite.Group()

        self.tmx_maps = tmx_importer('images', 'data', 'tmx', 'Tiled_files')
        self.map_data = self.tmx_maps['Dungeon1']

        self.setup()
    
    def setup(self):
        map_scale = 4
        current_tile_size = 16 * map_scale

        for layer in self.map_data.visible_layers:
            if hasattr(layer, 'data'):
                for x, y, surf in layer.tiles():
                    pos = (x * current_tile_size, y * current_tile_size)
                    Sprite(pos, surf, self.all_sprites)

        for obj in self.map_data.objects:
            if obj.name == 'Player':
                self.player = Player((obj.x * map_scale, obj.y * map_scale), self.all_sprites)

    def run(self, dt):
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.player.rect.center)