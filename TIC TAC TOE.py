import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
WHITE = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
CIRCLE_COLOR = (255, 0, 0)
CROSS_COLOR = (0, 0, 255)
GRID_SIZE = 3
SQUARE_SIZE = WIDTH // GRID_SIZE

# Initialize the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Initialize the game board
board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
player_turn = True  # True if it's player's turn, False if it's computer's turn
game_over = False   # True if the game is over

# Font for displaying messages
font = pygame.font.Font(None, 36)

# Function to draw the grid
def draw_grid():
    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

# Function to draw the X symbol
def draw_x(row, col):
    pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE),
                     ((col + 1) * SQUARE_SIZE, (row + 1) * SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, CROSS_COLOR, ((col + 1) * SQUARE_SIZE, row * SQUARE_SIZE),
                     (col * SQUARE_SIZE, (row + 1) * SQUARE_SIZE), LINE_WIDTH)

# Function to draw the O symbol
def draw_o(row, col):
    pygame.draw.circle(screen, CIRCLE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                       SQUARE_SIZE // 2 - LINE_WIDTH)

# Function to check if a player has won
def check_winner():
    # Check rows and columns
    for i in range(GRID_SIZE):
        if all(board[i][j] == 'X' for j in range(GRID_SIZE)) or all(board[j][i] == 'X' for j in range(GRID_SIZE)):
            return 'X'
        if all(board[i][j] == 'O' for j in range(GRID_SIZE)) or all(board[j][i] == 'O' for j in range(GRID_SIZE)):
            return 'O'

    # Check diagonals
    if all(board[i][i] == 'X' for i in range(GRID_SIZE)) or all(board[i][GRID_SIZE - 1 - i] == 'X' for i in range(GRID_SIZE)):
        return 'X'
    if all(board[i][i] == 'O' for i in range(GRID_SIZE)) or all(board[i][GRID_SIZE - 1 - i] == 'O' for i in range(GRID_SIZE)):
        return 'O'

    return None

# Function to check if the board is full
def is_board_full():
    return all(board[i][j] != '' for i in range(GRID_SIZE) for j in range(GRID_SIZE))

# Function to get AI move
def make_computer_move():
    # check if AI can win in the next move
    for i in range(GRID_SIZE * GRID_SIZE):
        if board[i // GRID_SIZE][i % GRID_SIZE] == '':
            board[i // GRID_SIZE][i % GRID_SIZE] = 'O'
            if check_winner() == 'O':
                return i
            board[i // GRID_SIZE][i % GRID_SIZE] = ''

    # check if player can win in the next move and block them
    for i in range(GRID_SIZE * GRID_SIZE):
        if board[i // GRID_SIZE][i % GRID_SIZE] == '':
            board[i // GRID_SIZE][i % GRID_SIZE] = 'X'
            if check_winner() == 'X':
                return i
            board[i // GRID_SIZE][i % GRID_SIZE] = ''

    # otherwise, make a random move
    while True:
        move = random.randint(0, GRID_SIZE * GRID_SIZE - 1)
        if board[move // GRID_SIZE][move % GRID_SIZE] == '':
            return move

# Function to reset the game state
def reset_game():
    global board, player_turn, game_over
    board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    player_turn = True
    game_over = False

# Function to display a message on the screen with specified text color
def display_message(message, text_color):
    text = font.render(message, True, text_color)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

# Main game loop
def main():
    global player_turn, game_over
    player_turn = True
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN and player_turn:
                    row = event.pos[1] // SQUARE_SIZE
                    col = event.pos[0] // SQUARE_SIZE
                    
                    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE and board[row][col] == '':
                        board[row][col] = 'X'
                        player_turn = not player_turn
                        
                        winner = check_winner()
                        if winner is not None:
                            #print(f"Player {winner} wins!")
                            game_over = True
                
                if not player_turn and not is_board_full() and not game_over:
                    computer_move = make_computer_move()
                    if computer_move is not None:
                        row, col = divmod(computer_move, GRID_SIZE)
                        board[row][col] = 'O'
                        player_turn = not player_turn
                        
                        winner = check_winner()
                        if winner is not None:
                            #print(f"Player {winner} wins!")
                            game_over = True
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RSHIFT:
                reset_game()
                game_over = False  # Reset game_over when restarting

        screen.fill(WHITE)
        draw_grid()

        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if board[i][j] == 'X':
                    draw_x(i, j)
                elif board[i][j] == 'O':
                    draw_o(i, j)

        winner = check_winner()
        if winner:
            text_color = (82, 139, 139, 255)
            display_message(f'Player {winner} wins! Press RSHIFT to restart.', text_color)
            game_over = True  # Set game_over to True when there is a winner
        elif is_board_full():
            text_color = (82, 139, 139, 255)
            display_message('It\'s a tie! Press RSHIFT to restart.', text_color)
            game_over = True  # Set game_over to True when it's a tie

        pygame.display.flip()

# Run the game
if __name__ == "__main__":
    main()
