from settings import *
from support import import_image, import_tilemap

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        
        # sprite sheet
        self.frames_dict = import_tilemap(24, 16, 'images', 'graphics', 'characters', 'blue_cat')

        self.animations = {
            'down':       [self.frames_dict[(col, 0)]  for col in range(12, 16)],
            'down_left':  [self.frames_dict[(col, 2)]  for col in range(12, 16)],
            'left':       [self.frames_dict[(col, 4)]  for col in range(12, 16)],
            'up_left':    [self.frames_dict[(col, 6)]  for col in range(12, 16)],
            'up':         [self.frames_dict[(col, 8)]  for col in range(12, 16)],
            'up_right':   [self.frames_dict[(col, 10)] for col in range(12, 16)],
            'right':      [self.frames_dict[(col, 12)] for col in range(12, 16)],
            'down_right': [self.frames_dict[(col, 14)] for col in range(12, 16)]
        }

        for state, frames in self.animations.items():
            self.animations[state] = [pygame.transform.scale_by(frame, 2) for frame in frames]

        self.status = 'down'
        self.frame_index = 0

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        # movement
        self.direction = pygame.Vector2()
        self.speed = 200

    def get_status(self):
        if self.direction.length() > 0:
            if self.direction.x > 0: # DIREITA
                if self.direction.y > 0: self.status = 'down_right'
                elif self.direction.y < 0: self.status = 'up_right'
                else: self.status = 'right'
            elif self.direction.x < 0: # ESQUERDA
                if self.direction.y > 0: self.status = 'down_left'
                elif self.direction.y < 0: self.status = 'up_left'
                else: self.status = 'left'
            else: # VERTICAL
                if self.direction.y > 0: self.status = 'down'
                else: self.status = 'up'

    def animate(self, dt):
        current_animatioin = self.animations[self.status]

        if self.direction.magnitude() != 0:
            self.frame_index += 10 * dt
            if self.frame_index >= len(current_animatioin):
                self.frame_index = 0
        else:
            self.frame_index = 0
        
        self.image = current_animatioin[int(self.frame_index)]
            

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def update(self, dt):
        self.input()
        self.get_status()
        self.rect.center += self.direction * self.speed * dt
        self.animate(dt)
