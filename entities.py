from settings import *
from support import import_image, import_tilemap

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        
        # sprite sheet
        self.frames_dict = import_tilemap(24, 16, 'images', 'graphics', 'characters', 'blue_cat')

        self.animations = {
            # down
            'down_idle':       [self.frames_dict[(0, 0)]],
            'down_walk':       [self.frames_dict[(col, 0)]  for col in range(12, 16)],
            'down_run':        [self.frames_dict[(col, 0)]  for col in range(16, 20)],
            
            # down left
            'down_left_idle':  [self.frames_dict[(0, 2)]],
            'down_left_walk':  [self.frames_dict[(col, 2)]  for col in range(12, 16)],
            'down_left_run':   [self.frames_dict[(col, 2)]  for col in range(16, 20)],
            
            # left
            'left_idle':       [self.frames_dict[(0, 4)]],
            'left_walk':       [self.frames_dict[(col, 4)]  for col in range(12, 16)],
            'left_run':        [self.frames_dict[(col, 4)]  for col in range(16, 20)],
            
            # up left
            'up_left_idle':    [self.frames_dict[(0, 6)]],
            'up_left_walk':    [self.frames_dict[(col, 6)]  for col in range(12, 16)],
            'up_left_run':     [self.frames_dict[(col, 6)]  for col in range(16, 20)],
            
            # up
            'up_idle':         [self.frames_dict[(0, 8)]],
            'up_walk':         [self.frames_dict[(col, 8)]  for col in range(12, 16)],
            'up_run':          [self.frames_dict[(col, 8)]  for col in range(16, 20)],
            
            # up right
            'up_right_idle':   [self.frames_dict[(0, 10)]],
            'up_right_walk':   [self.frames_dict[(col, 10)] for col in range(12, 16)],
            'up_right_run':    [self.frames_dict[(col, 10)] for col in range(16, 20)],
            
            # right
            'right_idle':      [self.frames_dict[(0, 12)]],
            'right_walk':      [self.frames_dict[(col, 12)] for col in range(12, 16)],
            'right_run':       [self.frames_dict[(col, 12)] for col in range(16, 20)],
            
            # down right
            'down_right_idle': [self.frames_dict[(0, 14)]],
            'down_right_walk': [self.frames_dict[(col, 14)] for col in range(12, 16)],
            'down_right_run':  [self.frames_dict[(col, 14)] for col in range(16, 20)]
        }

        for state, frames in self.animations.items():
            self.animations[state] = [pygame.transform.scale_by(frame, 2) for frame in frames]

        self.facing_direction = 'down'
        self.status = 'down_walk'
        self.frame_index = 0
        self.is_running = False

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        # movement
        self.direction = pygame.Vector2()
        self.speed = 200

    def get_status(self):
        if self.direction.length() > 0:
            if self.direction.x > 0: # DIREITA
                if self.direction.y > 0:   self.facing_direction = 'down_right'
                elif self.direction.y < 0: self.facing_direction = 'up_right'
                else:                      self.facing_direction = 'right'
            elif self.direction.x < 0: # ESQUERDA
                if self.direction.y > 0:   self.facing_direction = 'down_left'
                elif self.direction.y < 0: self.facing_direction = 'up_left'
                else:                      self.facing_direction = 'left'
            else: # VERTICAL
                if self.direction.y > 0:   self.facing_direction = 'down'
                elif self.direction.y < 0: self.facing_direction = 'up'

            suffix = '_run' if self.is_running else '_walk'
            self.status = self.facing_direction + suffix
        
        else:
            # parado
            self.status = self.facing_direction + '_idle'

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

        self.is_running = keys[pygame.K_SPACE]
        self.speed = 300 if self.is_running else 200

        self.direction = self.direction.normalize() if self.direction else self.direction

    def update(self, dt):
        self.input()
        self.get_status()
        self.rect.center += self.direction * self.speed * dt
        self.animate(dt)
