import game_logic
from game2dboard import Board

# Initialize the game board
board = Board(4, 4)
board.cell_size = 100
board.title = "2048 Game"
board.margin = 10
board.cell_spacing = 5

# Initialize the game state variables
mat = game_logic.start_game()
graph = game_logic.board_to_graph(mat)
game_over = False
score = 0
scores = []

def draw_board():
    """Draw the current game board on the UI."""
    for i in range(4):
        for j in range(4):
            value = mat[i][j]
            if value == 0:
                board[i][j] = 'empty.png'  # Path to the empty tile image
            else:
                board[i][j] = f'{value}.png'  # Path to numbered tile images
    board.title = f"2048 Game - Score: {score}"


def display_scoreboard(scores):
    """Display the top scores."""
    print("\nScoreboard:")
    for idx, sc in enumerate(scores):
        print(f"{idx + 1}. {sc}")
    print()


def key_press(key):
    """Handle key presses for game actions."""
    global mat, graph, game_over, score, scores
    key = key.lower()

    if game_over:
        if key == 'r':
            mat = game_logic.start_game()
            graph = game_logic.board_to_graph(mat)
            game_over = False
            score = 0
            draw_board()
            print("Game restarted! Continue playing.")
        elif key == 'e':
            board.close()
        else:
            print("Press 'r' to restart or 'e' to exit.")
        return

    if key == 'w':
        mat, changed, move_score = game_logic.move_up(mat)
    elif key == 's':
        mat, changed, move_score = game_logic.move_down(mat)
    elif key == 'a':
        mat, changed, move_score = game_logic.move_left(mat)
    elif key == 'd':
        mat, changed, move_score = game_logic.move_right(mat)
    else:
        return

    if changed:
        score += move_score
        game_logic.add_new_2(mat)
        graph = game_logic.board_to_graph(mat)
        draw_board()

        if game_logic.bfs_search_value(mat, graph, target=2048) == "WON":
            print("Congratulations! You won!")
            scores.append(score)
            game_logic.insertion_sort(scores)
            display_scoreboard(scores)
            print("Press 'r' to restart or 'e' to exit.")
            game_over
        elif game_logic.has_valid_moves(mat, graph) == "LOST":
            print("Game Over!")
            scores.append(score)
            game_logic.insertion_sort(scores)
            display_scoreboard(scores)
            print("Press 'r' to restart or 'e' to exit.")
            game_over = True
    else:
        # If no tiles moved, check for game over
        if game_logic.has_valid_moves(mat, graph) == "LOST":
            print("Game Over!")
            scores.append(score)
            game_logic.insertion_sort(scores)
            display_scoreboard(scores)
            print("Press 'r' to restart or 'e' to exit.")
            game_over = True


# Initial draw
# Create and initialize the custom board directly in 2048.py
mat = game_logic.create_custom_board([
    [2, 4, 8, 16],
    [32, 64, 128, 256],
    [512, 1024, 2048, 0],
    [0, 0, 0, 0]
])

# Initialize the graph for the custom board
graph = game_logic.board_to_graph(mat)

# Draw the custom board
draw_board()

board.on_key_press = key_press
board.show()
