from settings import *
from support import import_image, import_tilemap

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        
        # sprite sheet
        self.frames_dict = import_tilemap(24, 16, 'images', 'graphics', 'characters', 'blue_cat')

        self.animations = {}

        directions = ['down', 'down_left', 'left', 'up_left', 'up', 'up_right', 'right', 'down_right']
        rows = [0, 2, 4, 6, 8, 10, 12, 14]

        for direction, row in zip(directions, rows):
            # idle (parado em pé - coluna 0)
            self.animations[f'{direction}_idle'] = [self.frames_dict[(0, row)]]
            # sit (sentar - colunas 0 a 3)
            extra_sit_frames = range(0, 3) if row in [0, 8] else range(0, 2)
            self.animations[f'{direction}_sit'] = [self.frames_dict[(col, row)] for col in range(0, 4)] + \
                                                   [self.frames_dict[(col, row + 1)] for col in extra_sit_frames]
            # walk (caminhada - colunas 12 a 15)
            self.animations[f'{direction}_walk'] = [self.frames_dict[(col, row)] for col in range(12, 16)]
            # run (corrida - colunas 16 a 19)
            self.animations[f'{direction}_run'] = [self.frames_dict[(col, row)] for col in range(16, 20)] + \
                                                   [self.frames_dict[(16, row + 1)]]

        for state, frames in self.animations.items():
            self.animations[state] = [pygame.transform.scale_by(frame, 2) for frame in frames]

        self.status = 'down_idle'
        self.old_status = self.status
        self.facing_direction = 'down'
        self.frame_index = 0

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        # movement
        self.direction = pygame.Vector2()
        self.speed = 200
        self.is_running = False

        # timers
        self.sit_timer = 0
        self.sit_duration = 3.0 # tempo para o gato sentar

    def get_status(self):
        if self.direction.x > 0:
            if self.direction.y > 0:   self.facing_direction = 'down_right'
            elif self.direction.y < 0: self.facing_direction = 'up_right'
            else:                      self.facing_direction = 'right'
        elif self.direction.x < 0:
            if self.direction.y > 0:   self.facing_direction = 'down_left'
            elif self.direction.y < 0: self.facing_direction = 'up_left'
            else:                      self.facing_direction = 'left'
        elif self.direction.y > 0:     self.facing_direction = 'down'
        elif self.direction.y < 0:     self.facing_direction = 'up'

        if self.direction.length() > 0:
            self.sit_timer = 0
            suffix = '_run' if self.is_running else '_walk'
            self.status = self.facing_direction + suffix
        else:
            if self.sit_timer < self.sit_duration:
                self.status = self.facing_direction + '_idle'
            else:
                self.status = self.facing_direction + '_sit'

        if self.status != self.old_status:
            self.frame_index = 0
            self.old_status = self.status

    def animate(self, dt):
        current_animation = self.animations[self.status]

        self.frame_index += 10 * dt

        if self.frame_index >= len(current_animation):
            if '_sit' in self.status:
                self.frame_index = len(current_animation) - 1
            else:
                self.frame_index = 0
            
        self.image = current_animation[int(self.frame_index)]
            

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])

        self.is_running = keys[pygame.K_SPACE]
        self.speed = 300 if self.is_running else 200

        self.direction = self.direction.normalize() if self.direction else self.direction

    def update(self, dt):
        self.input()

        if self.direction.length() == 0:
            self.sit_timer += dt

        self.get_status()
        self.rect.center += self.direction * self.speed * dt
        self.animate(dt)
