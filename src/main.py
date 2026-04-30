import pygame

from src.core.game import Game


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    game = Game()

    while game.running:
        # Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # Render
        screen.fill("purple")
        rect = pygame.Rect(100, 100, 100, 100)
        pygame.draw.rect(screen, (255, 255, 255), rect)
        # Show
        pygame.display.flip()
        # Delta time
        clock.tick(60)

    pygame.quit()