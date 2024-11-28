import random
from collections import defaultdict, deque

# Initialize the game board with two tiles
def start_game():
    """Initialize a 4x4 game board with two starting tiles."""
    mat = [[0] * 4 for _ in range(4)]
    add_new_2(mat)
    add_new_2(mat)
    return mat


def add_new_2(mat):
    """Add a new tile (2 or 4) to a random empty cell."""
    r, c = random.randint(0, 3), random.randint(0, 3)
    while mat[r][c] != 0:  # Ensure the cell is empty
        r, c = random.randint(0, 3), random.randint(0, 3)
    mat[r][c] = 2 if random.random() < 0.9 else 4


def board_to_graph(mat):
    """Convert the game board into a graph represented as an adjacency list."""
    rows, cols = len(mat), len(mat[0])
    graph = defaultdict(list)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up

    for i in range(rows):
        for j in range(cols):
            for dx, dy in directions:
                x, y = i + dx, j + dy
                if 0 <= x < rows and 0 <= y < cols:
                    graph[(i, j)].append((x, y))
    return graph


def has_valid_moves(mat, graph):
    """Check if there are valid moves left using graph traversal."""
    for node, neighbors in graph.items():
        i, j = node
        for x, y in neighbors:
            if mat[x][y] == mat[i][j] or mat[x][y] == 0:  # Mergeable or empty cell
                return "GAME NOT OVER"
    return "LOST"


def bfs_search_value(mat, graph, target=2048):
    """Search for a target value (e.g., 2048) using BFS."""
    visited = set()
    queue = deque([(i, j) for i in range(4) for j in range(4)])  # Start from all cells

    while queue:
        i, j = queue.popleft()
        if (i, j) in visited:
            continue
        visited.add((i, j))

        if mat[i][j] == target:
            return "WON"

        for x, y in graph[(i, j)]:
            if (x, y) not in visited:
                queue.append((x, y))

    return "CONTINUE"


def compress(mat):
    """Compress the board by moving all non-zero values to the left."""
    changed = False
    new_mat = []
    for row in mat:
        filtered = [num for num in row if num != 0]
        new_row = filtered + [0] * (4 - len(filtered))
        if new_row != row:
            changed = True
        new_mat.append(new_row)
    return new_mat, changed


def merge(mat):
    """Merge adjacent tiles with the same value."""
    changed = False
    score = 0
    for row in mat:
        for j in range(3):
            if row[j] != 0 and row[j] == row[j + 1]:
                row[j] *= 2
                score += row[j]
                row[j + 1] = 0
                changed = True
    return mat, changed, score


def reverse(mat):
    """Reverse each row of the board."""
    return [row[::-1] for row in mat]


def transpose(mat):
    """Transpose the board."""
    return [list(row) for row in zip(*mat)]


def move_left(mat):
    """Move tiles left."""
    mat, changed1 = compress(mat)
    mat, changed2, score = merge(mat)
    mat, _ = compress(mat)
    return mat, changed1 or changed2, score


def move_right(mat):
    """Move tiles right."""
    mat = reverse(mat)
    mat, changed, score = move_left(mat)
    mat = reverse(mat)
    return mat, changed, score


def move_up(mat):
    """Move tiles up."""
    mat = transpose(mat)
    mat, changed, score = move_left(mat)
    mat = transpose(mat)
    return mat, changed, score


def move_down(mat):
    """Move tiles down."""
    mat = transpose(mat)
    mat, changed, score = move_right(mat)
    mat = transpose(mat)
    return mat, changed, score


def insertion_sort(arr):
    """Sort scores in descending order using insertion sort."""
    for i in range(1, len(arr)):
        key_item = arr[i]
        j = i - 1
        while j >= 0 and arr[j] < key_item:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key_item