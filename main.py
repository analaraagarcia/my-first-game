from settings import *
from entities import Player
from level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('The Game With No Name')
        self.clock = pygame.time.Clock()

        self.level = Level()

    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.display_surface.fill('black')

            self.level.run(dt)

            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()