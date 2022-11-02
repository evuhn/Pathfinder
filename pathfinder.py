import pygame
from astar import aStar
from game_board import *
from dijkstra import dijkstra

def main(window, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    startNode = None
    endNode = None

    run = True #while the application is running

    #main loop for while game is running
    while(run):
        draw(window, grid, ROWS, width)

        #event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #when the x in top right is clicked
                run = False

            if pygame.mouse.get_pressed()[0]: #left mouse click
                pos = pygame.mouse.get_pos() #gives us position of the pygame mouse on the window, the (x, y) position
                row, col = get_click_pos(pos, ROWS, width)
                if not startNode and grid[row][col] != endNode:
                    startNode = grid[row][col]
                    grid[row][col].set_start()
                
                elif not endNode and grid[row][col] != startNode:
                    endNode = grid[row][col]
                    grid[row][col].set_end()

                elif grid[row][col] != startNode and grid[row][col] !=endNode:
                    grid[row][col].set_blocked()

            elif pygame.mouse.get_pressed()[2]: #right mouse click
                pos = pygame.mouse.get_pos()
                row, col = get_click_pos(pos, ROWS, width)
                grid[row][col].reset()
                if grid[row][col] == startNode:
                    startNode = None
                
                elif grid[row][col] == endNode:
                    endNode = None
            
            if event.type == pygame.KEYDOWN:
                if startNode and endNode: #can begin search if start and end have been assigned
                    for row in grid:
                            for node in row:
                                node.update_neighbors(grid)

                if event.key == pygame.K_a: #does a* algorithm if 'a' is pressed
                    aStar(lambda: draw(window, grid, ROWS, width), grid, startNode, endNode)
                
                if event.key == pygame.K_d: #does dijkstras if 'd' is pressed
                    dijkstra(lambda: draw(window, grid, ROWS, width), grid, startNode, endNode)

                if event.key == pygame.K_r: #r key resets the board
                    endNode = None
                    startNode = None
                    grid = make_grid(ROWS, width)

    pygame.quit()

main(WINDOW, WIDTH)