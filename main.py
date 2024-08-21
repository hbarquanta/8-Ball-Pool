import pygame
from config import *
from game_logic import Game
from gui import GameGUI

def main():
    pygame.init()
    screen = pygame.display.set_mode((TABLE_WIDTH, TABLE_HEIGHT + 100))
    pygame.display.set_caption("2-Player Pool Game")
    
    game = Game()
    gui = GameGUI(screen, game)
    
    clock = pygame.time.Clock()

    while game.running:
        gui.handle_events()
        
        # Update the game state
        game.update()

        # Clear the screen and draw everything
        screen.fill(GREEN)
        gui.render()

        # Update the display
        pygame.display.flip()

        # Limit the frame rate
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()
