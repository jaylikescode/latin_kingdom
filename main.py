import pygame
import sys
from game import Game

def main():
    # Initialize Pygame
    pygame.init()
    
    # Create and run the game
    game = Game()
    game.start_wave()
    
    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    game.handle_mouse_down(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left click release
                    game.handle_mouse_up(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                game.handle_mouse_motion(event.pos)
            elif event.type == pygame.KEYDOWN:
                if game.game_over:
                    if event.key == pygame.K_r:
                        game.restart()
                        game.start_wave()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                        
        game.update()
        game.draw()
        game.clock.tick(60)  # 60 FPS

if __name__ == "__main__":
    main()
