from settings import *
from entities import Player

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('The Game With No Name')
        self.clock = pygame.time.Clock()

        # groups
        self.all_sprites = pygame.sprite.Group()

        self.player = Player(self.all_sprites)

    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.all_sprites.update(dt)
            
            self.display_surface.fill('black')
            self.all_sprites.draw(self.display_surface)

            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()