import pygame

pygame.init()

#this is for setting up the window size of the application
WIDTH = 800
WINDOW = pygame.display.set_mode((WIDTH, WIDTH)) #sets the size of the window
pygame.display.set_caption("Pathfinder")

#rgb values for colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0 ,0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0 ,255)
GRAY = (128, 128, 128)

class Node:
    def __init__(self, row, col, nodeWidth, totalRows):
        self.row = row
        self.col = col
        self.color = WHITE
        self.x = row * nodeWidth #this is the (x, y) coordinate on the screen, different from the (row, col) position.
        self.y = col * nodeWidth #not sure if width should be parameter or use the global = no bc this is the width of the node, not the window width (which is the global)
        self.width = nodeWidth
        self.neighbors = []
        self.totalRows = totalRows #used in the method update_neighbors()

    #some getters and setters
    def is_open(self):
        return self.color == YELLOW
    
    def set_open(self):
        self.color = YELLOW

    def is_closed(self):
        return self.color == RED
    
    def set_closed(self):
        self.color = RED

    def is_start(self):
        return self.color == GREEN
    
    def set_start(self):
        self.color = GREEN
    
    def is_end(self):
        return self.color == MAGENTA
    
    def set_end(self):
        self.color = MAGENTA
    
    def is_blocked(self):
        return self.color == BLACK

    def set_blocked(self):
        self.color = BLACK
    
    def reset(self):
        self.color = WHITE
    
    def set_path(self):
        self.color = CYAN
    
    def get_pos(self):
        return self.row, self.col #why not x and y?

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width)) #to draw the node on the window
    
    def update_neighbors(self, grid):
        #bottom neighbor
        if self.row + 1 < self.totalRows and not grid[self.row + 1][self.col].is_blocked():
            self.neighbors.append(grid[self.row + 1][self.col])
        
        #top neighbor
        if self.row - 1 >= 0 and not grid[self.row - 1][self.col].is_blocked():
            self.neighbors.append(grid[self.row - 1][self.col])

        #right neighbor
        if self.col + 1 < self.totalRows and not grid[self.row][self.col + 1].is_blocked():
            self.neighbors.append(grid[self.row][self.col + 1])

        #left neighbor
        if self.col - 1 >= 0 and not grid[self.row][self.col - 1].is_blocked():
            self.neighbors.append(grid[self.row][self.col - 1])       

#THIS IS FOR THE INSTRUCTION MENU
# instructions = """Welcome to my pathfinding application!
# To begin, create a starting point with your first click
# Your next click will be the ending point
# Once you have a start and end, you can draw obstacles by clicking on empty spots
# press Space to begin the pathfinding algorithm
# When the algorithm has finished, press "r" to reset the grid"""

# font = pygame.font.SysFont("arial.ttf", 32)

# text = font.render(instructions, BLACK, WHITE)

# textRect = text.get_rect()

# textRect.center = (WIDTH//2, WIDTH//2)

# def draw_text():
#     pass

def create_path(draw, came_from, current):
    while current in came_from:
        current = came_from[current]
        current.set_path()
        draw()
    current.set_start()

def make_grid(rows, gridWidth):
    grid = []
    gap = gridWidth // rows #the gap is the width of the cubes in the grid
    for row in range(rows):
        grid.append([]) #adds an empty list cell for each row
        for col in range(rows):
            node = Node(row, col, gap, rows)
            grid[row].append(node) #this adds the nodes into each row

    return grid

#draws the grid lines
def draw_grid(window, rows, gridWidth):
    gap = gridWidth // rows #the gap is the width of the cubes in the grid aka how far apart the grid lines are from each other
    for row in range(rows):
        pygame.draw.line(window, GRAY, (0, row * gap), (gridWidth, row * gap)) #this is going to draw the horizontal grid lines
        for col in range(rows):
            pygame.draw.line(window, GRAY, (col * gap, 0), (col * gap, gridWidth)) #this is going to draw the vertical grid lines

#draws the window
def draw(window, grid, rows, width):
    window.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(window)

    draw_grid(window, rows, width)
    pygame.display.update() #tells the application to update the screen with what we have drawn


def get_click_pos(pos, rows, gridWidth):
    gap = gridWidth // rows
    y, x = pos #pos is from pygame.mouse.get_pos() which returns (x, y)              !!!!QUESTION!!!! why is this y, x instead of x, y?
    row = y // gap #divide the (x , y) coordinate by width of the gaps to find the row and col pos
    col = x // gap

    return row, col