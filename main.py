import pygame
from pygame.locals import *


##### Globals #####

# Starting the game with X
XO = 'X'

# Initialize the grid/board
grid = [[ None, None, None ],
        [ None, None, None ], 
        [ None, None, None ]]

winner = None
running = 1
won = False



def evaluate_move():
    '''
    Evaluate each move in the grid  
    '''

    global grid

    for row in range(0, len(grid)):  
        if grid[row][0] == grid[row][1] and grid[row][1] == grid[row][2]:  
           
            if grid[row][0] == 'X': 
                return 10 
            elif grid[row][0] == 'O':  
                return - 10 
  
    for col in range(0, len(grid)):  
        if grid[0][col] == grid[1][col] and grid[1][col] == grid[2][col]:  
           
            if grid[0][col]=='X': 
                return 10 
            elif grid[0][col] == 'O':  
                return - 10 
  
    if grid[0][0] == grid[1][1] and grid[1][1] == grid[2][2]:  
       
        if grid[0][0] == 'X':  
            return 10 
        elif grid[0][0] == 'O':  
            return - 10 
       
    if grid[0][2] == grid[1][1] and grid[1][1] == grid[2][0]:  
       
        if grid[0][2] == 'X':  
            return 10 
        elif grid[0][2] == 'O':  
            return - 10 
   
    return 0 


def are_moves_left():
    '''
    Check if any moves are left  
    '''

    global grid

    for i in range(0, len(grid)):
        for j in range(0, len(grid)):
            if grid[i][j] == None:
                return True
    
    return False


def minimax(depth, player_type):
    '''
    Run the Mini-Max algorithm 
    '''
    global grid, count

    score = evaluate_move()

    if score == 10:
        return score 
  
    if score == -10: 
        return score

    if not are_moves_left():
        return 0  

    if player_type:
        best_val = - 10_000
        for i in range(0, len(grid)):
            for j in range(0, len(grid)):
                if grid[i][j] == None:
                    grid[i][j] = XO
                    value = minimax(depth + 1, not player_type)
                    best_val = max(best_val, value) 
                    grid[i][j] = None

    else:
        best_val = 10_000
        for i in range(0, len(grid)):
            for j in range(0, len(grid)):
                if grid[i][j] == None: 
                    grid[i][j] = XO       
                    value = minimax(depth + 1, not player_type)
                    best_val = min(best_val, value)  
                    grid[i][j] = None
    
    return best_val


def get_best_move(Piece):
    '''
    Get the best possible move for X/O  
    '''

    best_move_val = - 10_000
    x = 0
    y = 0

    if(Piece == 'X'):
        is_max = True
    else:
        is_max = False

    for i in range(0, len(grid)):
        for j in range(0, len(grid)):
            if grid[i][j] == None:
                grid[i][j] = XO
                value = minimax(0, is_max)
                grid[i][j] = None

                if best_move_val < value:
                    x = i
                    y = j
                    best_move_val = value
    return x, y


def init_board(ttt):
    '''
    Initialize the board 
    '''

    background = pygame.Surface(ttt.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    pygame.draw.line(background, (0,0,0), (100, 0), (100, 300), 2)
    pygame.draw.line(background, (0,0,0), (200, 0), (200, 300), 2)

    pygame.draw.line(background, (0,0,0), (0, 100), (300, 100), 2)
    pygame.draw.line(background, (0,0,0), (0, 200), (300, 200), 2)

    return background


def draw_status(board):
    '''
    Print the current status of AI  
    '''

    global XO, winner

    if winner is None:
        message = XO + '\'s turn. AI is thinking...'
    else:
        message = winner + ' won!'
        
    font = pygame.font.Font(None, 24)
    text = font.render(message, 1, (10, 10, 10))

    board.fill((250, 250, 250), (0, 300, 300, 25))
    board.blit(text, (10, 300))


def show_board(ttt, board):
    '''
    Show the board  
    '''

    draw_status(board)
    ttt.blit(board, (0, 0))
    pygame.display.flip()


def drawMove(board, boardCol, boardRow):
    '''
    Draw the chosen move on the board 
    '''

    global XO

    centerX = ((boardCol) * 100) + 50
    centerY = ((boardRow) * 100) + 50

    if (XO == 'O'):
        pygame.draw.circle (board, (0,0,0), (centerX, centerY), 42, 2)
    else:
        pygame.draw.line(board, (0,0,0), (centerX - 22, centerY - 22), (centerX + 22, centerY + 22), 2)
        pygame.draw.line(board, (0,0,0), (centerX + 22, centerY - 22), (centerX - 22, centerY + 22), 2)

    
def check_if_won(board):
    '''
    Check if X/O have won  
    '''

    global grid, winner, running, won

    for row in range (0, 3):
        if ((grid [row][0] == grid[row][1] == grid[row][2]) and (grid [row][0] is not None)):
            winner = grid[row][0]
            pygame.draw.line (board, (250,0,0), (0, (row + 1)*100 - 50), (300, (row + 1)*100 - 50), 2)
            won = True 
            break

    for col in range (0, 3):
        if (grid[0][col] == grid[1][col] == grid[2][col]) and (grid[0][col] is not None):
            winner = grid[0][col]
            pygame.draw.line (board, (250,0,0), ((col + 1)* 100 - 50, 0), ((col + 1)* 100 - 50, 300), 2)
            won = True
            break

    if (grid[0][0] == grid[1][1] == grid[2][2]) and (grid[0][0] is not None):
        winner = grid[0][0]
        pygame.draw.line(board, (250,0,0), (50, 50), (250, 250), 2)
        won = True

    if (grid[0][2] == grid[1][1] == grid[2][0]) and (grid[0][2] is not None):
        winner = grid[0][2]
        pygame.draw.line(board, (250,0,0), (250, 50), (50, 250), 2)
        won = True


def change():
    '''
    Switch between X and 0  
    '''

    global XO

    if XO == 'X':
        XO = 'O'
    else:
        XO = 'X'



if __name__ == '__main__':
    '''
    Main function  
    '''

    pygame.init()
    ttt = pygame.display.set_mode ((300, 325))
    pygame.display.set_caption ('Tic-Tac-Toe-AI')

    board = init_board(ttt)
    running = 1

    while running:

        for event in pygame.event.get():
            if event.type is QUIT:
                running = 0
        
        check_if_won(board)
        
        if not won:
            x, y = get_best_move(XO)
            grid[x][y] = XO
            draw_status(board)
            pygame.time.wait(3000)
            drawMove(board, x, y)
            change()
            show_board(ttt, board)
        else:
            show_board(ttt, board)
