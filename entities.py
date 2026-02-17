from settings import *
from support import import_image, import_tilemap

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        
        # sprite sheet
        self.frames_dict = import_tilemap(24, 16, 'images', 'graphics', 'characters', 'white_grey_cat')

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
            
            # looking around (olhando - colunas 4 a 7 e linha abaixo)
            looking_ida = [self.frames_dict[(col, row)] for col in range(4, 8)] + [self.frames_dict[(4, row + 1)]]
            looking_volta = looking_ida[-2:0:-1] 
            self.animations[f'{direction}_looking'] = looking_ida + looking_volta
            
            # laying down (deitando - colunas 8 a 11 e linha abaixo)
            self.animations[f'{direction}_lay'] = [self.frames_dict[(col, row)] for col in range(8, 12)] + \
                                                   [self.frames_dict[(col, row + 1)] for col in range(8, 12)]

            # walk (caminhada - colunas 12 a 15)
            self.animations[f'{direction}_walk'] = [self.frames_dict[(col, row)] for col in range(12, 16)]
            
            # run (corrida - colunas 16 a 19 e linha abaixo)
            self.animations[f'{direction}_run'] = [self.frames_dict[(col, row)] for col in range(16, 20)] + \
                                                   [self.frames_dict[(16, row + 1)]]

        for state, frames in self.animations.items():
            self.animations[state] = [pygame.transform.scale_by(frame, 2) for frame in frames]

        self.status = 'down_idle'
        self.old_status = self.status
        self.facing_direction = 'down'
        self.frame_index = 0

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_frect(center = pos)

        # movement
        self.direction = pygame.Vector2()
        self.speed = 200
        self.is_running = False
        self.looking = False
        self.laying = False

        # timers
        self.sit_timer = 0
        self.sit_duration = 3.0 # tempo para o gato sentar

    def get_status(self):
        if self.direction.length() > 0.5:
            self.sit_timer = 0
            
            # diagonais
            if abs(self.direction.x) > 0.4 and abs(self.direction.y) > 0.4:
                if self.direction.x > 0 and self.direction.y > 0:   self.facing_direction = 'down_right'
                elif self.direction.x > 0 and self.direction.y < 0: self.facing_direction = 'up_right'
                elif self.direction.x < 0 and self.direction.y > 0: self.facing_direction = 'down_left'
                elif self.direction.x < 0 and self.direction.y < 0: self.facing_direction = 'up_left'
            # retas
            else:
                if self.direction.x > 0:   self.facing_direction = 'right'
                elif self.direction.x < 0: self.facing_direction = 'left'
                elif self.direction.y > 0: self.facing_direction = 'down'
                elif self.direction.y < 0: self.facing_direction = 'up'

        if self.direction.length() > 0:
            suffix = '_run' if self.is_running else '_walk'
            self.status = self.facing_direction + suffix
        else:
            if self.looking:
                self.status = self.facing_direction + '_looking'
                self.sit_timer = 0
            elif self.laying:
                self.status = self.facing_direction + '_lay'
                self.sit_timer = 0
            elif self.sit_timer < self.sit_duration:
                self.status = self.facing_direction + '_idle'
            else:
                self.status = self.facing_direction + '_sit'

        if self.status != self.old_status:
            self.frame_index = 0
            self.old_status = self.status

    def animate(self, dt):
        current_animation = self.animations[self.status]

        if '_looking' in self.status:
            animation_speed = 4
        elif '_run' in self.status:
            animation_speed = 12
        else:
            animation_speed = 10
            
        self.frame_index += animation_speed * dt

        if self.frame_index >= len(current_animation):
            if '_sit' in self.status or '_lay' in self.status:
                self.frame_index = len(current_animation) - 1
            else:
                self.frame_index = 0
            
        self.image = current_animation[int(self.frame_index)]
            
    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])

        self.is_running = keys[pygame.K_SPACE]
        self.looking = keys[pygame.K_LSHIFT]
        self.laying = keys[pygame.K_s]

        self.speed = 300 if self.is_running else 200

        self.direction = self.direction.normalize() if self.direction else self.direction

    def update(self, dt):
        self.input()

        if self.direction.length() == 0 and not self.looking and not self.laying:
            self.sit_timer += dt

        self.get_status()
        self.rect.center += self.direction * self.speed * dt
        self.animate(dt)
