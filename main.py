
import pygame as pg

from manager import Manager
import settings


def main():
    """
    Main game loop for the Building Floor simulation.
    The loop runs continuously until the user quits the game.
    """
    manager = Manager()

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False 

            elif event.type == pg.MOUSEBUTTONDOWN:
                manager.check_floor_click(event.pos)
            
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    running = False

        manager.screen.fill((255, 255, 255)) 
        manager.update()
        manager.draw()
        pg.display.flip()
    
    pg.quit()


if __name__ == "__main__":
    main()
