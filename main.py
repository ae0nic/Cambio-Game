import pygame

WIDTH = 640
HEIGHT = 480

def main():
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(0xCFB5B0)
        pygame.display.update()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
