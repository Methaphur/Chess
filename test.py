import pygame 
import numpy as np


rows , cols = 8 ,8 
width , height = 504 , 504
white = (255, 255, 255)
black = (0, 0, 0)
cell_size = width//cols

def init_board():
    return np.zeros((8,8),dtype = str)
   
def drawboard(screen,board):
    rows, cols = board.shape
    for row in range(rows):
        for col in range(cols):
            color = white if (row + col) % 2 == 0 else black
            pygame.draw.rect(screen,color,(col * cell_size, row * cell_size, cell_size, cell_size))

def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Chess")

    board = init_board() 
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False



            drawboard(screen,board)

         # Updating the display
        pygame.display.flip()

     # Quitting the game
    pygame.quit()
    
main()