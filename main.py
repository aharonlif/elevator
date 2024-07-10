
import pygame as pg

from manager import Manager
import global_vars


def main():
    """
    Main game loop for the Building Floor simulation.
    The loop runs continuously until the user quits the game.
    """
    manager = Manager()
    last_iteration = 0
    running = True
    
    while running:
        ticks = pg.time.get_ticks()
        global_vars.ELAPSED_TIME = (ticks - last_iteration)/1000
        last_iteration = ticks
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    running = False

            elif event.type == pg.MOUSEBUTTONDOWN:
                manager.check_click(event.pos)
            
        manager.screen.fill((255, 255, 255)) 
        manager.update()
        manager.draw()
        pg.display.flip()
    
    pg.quit()


if __name__ == "__main__":
    main()
