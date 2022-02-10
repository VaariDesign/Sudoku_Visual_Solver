import sys
import time
import pygame



# 2 - Define constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
BLACK = (0, 0, 0)
WHITE = (255,255,255)


global window, rows, base_font
rows = 9



#sud = [[2, 5, 0, 0, 3, 0, 9, 0, 1],
#       [0, 1, 0, 0, 0, 4, 0, 0, 0],
#       [4, 0, 7, 0, 0, 0, 2, 0, 8],
#       [0, 0, 5, 2, 0, 0, 0, 0, 0],
#       [0, 0, 0, 0, 9, 8, 1, 0, 0],
#       [0, 4, 0, 0, 0, 3, 0, 0, 0],
#       [0, 0, 0, 3, 6, 0, 0, 7, 2],
#       [0, 7, 0, 0, 0, 0, 0, 0, 3],
#       [9, 0, 3, 0, 0, 0, 6, 0, 4]]

sud = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0]]



# 3 - Initialize the world
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()  # set the speed (frames per second)
pygame.display.set_caption('Sudoku')  # window name


## Screen
def grid(window, rows):
    """
    Draws sudoku background to window and returns grid size

    :param window: Game window
    :param rows: How many row and colum is wanted
    :return: Size of 1 grid x and y
    """
    yrow_size = window.get_height() / rows
    xrow_size = window.get_width() / rows
    x = 0
    y = 0
    pygame.draw.rect(window, (0,0,0), ((0,0), (window.get_width(),window.get_height())))
    pygame.draw.rect(window, (255,255,255), ((5,5), ((window.get_width()-10),(window.get_height()-10))))

    for l in range(rows):
        x += xrow_size
        y += yrow_size
        if ((l+1) % 3 == 0):
            pygame.draw.line(window, (0,0,0), (x-1,0), (x-1,window.get_height()))
            pygame.draw.line(window, (0,0,0), (x,0), (x,window.get_height()))
            pygame.draw.line(window, (0,0,0), (x+1,0), (x+1,window.get_height()))
            pygame.draw.line(window, (0,0,0), (0,y-1), (window.get_width(),y-1))
            pygame.draw.line(window, (0,0,0), (0,y), (window.get_width(),y))
            pygame.draw.line(window, (0,0,0), (0,y+1), (window.get_width(),y+1))
        else:
            pygame.draw.line(window, (0,0,0), (x,0), (x,window.get_height()))
            pygame.draw.line(window, (0,0,0), (0,y), (window.get_width(),y))

    return yrow_size,xrow_size


def shownumbers(sud,x,y):
    """
    Draws numbers in game window
    :param sud: Sudoku list
    :param x: Width of one grid
    :param y: Height of one grid
    :return:
    """
    h = 0
    for i in range(9):
        h += y
        w = x
        for j in range(9):
            number_surface = base_font.render(str(sud[i][j]),True,(0,0,0))
            if sud[i][j] != 0:
                window.blit(number_surface,(((w - x/2)-number_surface.get_width()/2),((h - y/2)-number_surface.get_height()/2)))
            w += x

def click_screen(x,y,sud):
    """
    Check which grid is pushed and change the number in that grid.
    Left mouse click increase number and right decrease.
    :param x: Width of grid
    :param y: Height of grid
    :param sud: Sudoku data list
    """
    if event.type == pygame.MOUSEBUTTONDOWN:
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            sud[int(pos[1]//y)][int(pos[0]//x)] += 1
            if sud[int(pos[1]//y)][int(pos[0]//x)] == 10:
                sud[int(pos[1]//y)][int(pos[0]//x)] = 0
            print(int(pos[0] // x), int(pos[1] // y))
        elif pygame.mouse.get_pressed()[2]:
            pos = pygame.mouse.get_pos()
            sud[int(pos[1]//y)][int(pos[0]//x)] -= 1
            if sud[int(pos[1]//y)][int(pos[0]//x)] == -1:
                sud[int(pos[1]//y)][int(pos[0]//x)] = 9
            print(int(pos[0] // x), int(pos[1] // y))



#Solver

def solve(sud, row, col, num):
# Check if same number is in row
    for x in range(9):
        if sud[row][x] == num:
            return False
# Check if same number is in Col
    for x in range(9):
        if sud[x][col] == num:
            return False

# Check if same number is in square
    srow = row - row % 3
    scol = col - col % 3
    for i in range(3):
        for j in range(3):
            if sud[i + srow][j + scol] == num:
                return False
    return True

def Suduko(sud, row, col):
    if (row == rows - 1 and col == rows):
        return True
    if col == rows:
        row += 1
        col = 0
    if sud[row][col] > 0:
        return Suduko(sud, row, col + 1)
    for num in range(1, rows + 1, 1):

        if solve(sud, row, col, num):

            sud[row][col] = num
#Comment next 3 lines for faster sollution, but no visualisation
            y,x = grid(window, 9)
            shownumbers(sud,x,y)
            pygame.display.flip()
            if Suduko(sud, row, col + 1):
                return True
        sud[row][col] = 0
    return False



# 6 - Loop forever
game = True
while game:
    # draw grid and numbers based on window size
    y,x = grid(window, rows)
    base_font = pygame.font.Font('fontti.ttf',int(y))
    shownumbers(sud,x,y)
# Middle click will solve the sudoku
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        click_screen(x,y,sud)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[1]:
                start= time.time()
                if (Suduko(sud, 0, 0)):
                    print("Solution does exist:)")

                else:
                    print("Solution does not exist:(")

                elapsed = time.time()-start
                print(elapsed)

    pygame.display.flip()

