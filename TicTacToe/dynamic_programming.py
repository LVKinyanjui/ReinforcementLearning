from collections import deque

def board_to_string(board):
    return ''.join(''.join(row) for row in board)

def string_to_board(s):
    return tuple(tuple(s[i:i+3]) for i in (0,3,6))

def is_winner(board, player):
    # Check rows, columns, and diagonals
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or \
           all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or \
       all(board[i][2-i] == player for i in range(3)):
        return True
    return False

def get_next_states(board, player):
    states = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == '.':
                new_board = list(list(row) for row in board)
                new_board[i][j] = player
                states.append(tuple(tuple(row) for row in new_board))
    return states

def value_iteration(epsilon=0.0001):
    # Initialize value function
    V = {}
    initial = tuple(tuple('.' * 3) for _ in range(3))
    
    # First pass: enumerate all states and set terminal values
    queue = deque([(initial, 'X')])
    while queue:
        board, player = queue.pop()
        board_str = board_to_string(board)
        if board_str in V:
            continue
            
        # Set initial values for terminal states
        if is_winner(board, 'X'):
            V[board_str] = 1.0
        elif is_winner(board, 'O'):
            V[board_str] = -1.0
        elif '.' not in board_str:  # Draw
            V[board_str] = 0.0
        else:
            V[board_str] = 0.0  # Initial guess for non-terminal states
            next_player = 'O' if player == 'X' else 'X'
            for next_board in get_next_states(board, player):
                queue.appendleft((next_board, next_player))
    
    # Value iteration
    delta = float('inf')
    while delta > epsilon:
        delta = 0
        for board_str in V.keys():
            if board_str not in V:
                continue
            
            board = string_to_board(board_str)
            old_v = V[board_str]
            
            # Skip terminal states
            if is_winner(board, 'X') or is_winner(board, 'O') or '.' not in board_str:
                continue
            
            # Determine whose turn it is
            x_count = board_str.count('X')
            o_count = board_str.count('O')
            player = 'X' if x_count == o_count else 'O'
            
            # Get value based on minimax principle
            next_values = [V[board_to_string(s)] for s in get_next_states(board, player)]
            if next_values:
                V[board_str] = max(next_values) if player == 'X' else min(next_values)
                
            delta = max(delta, abs(old_v - V[board_str]))
    
    return V

# Run value iteration
V = value_iteration()

# Print some example states
empty_board = board_to_string(tuple(tuple('.' * 3) for _ in range(3)))
print(f"Value of empty board: {V[empty_board]}")

# Print a few interesting positions
interesting_positions = [
    "X..O.....",  # Center defense
    "X...O....",  # Corner vs center
    "XX.OO....",  # Forced block
]

for pos in interesting_positions:
    print(f"\nPosition:\n{pos[0:3]}\n{pos[3:6]}\n{pos[6:9]}")
    print(f"Value: {V[pos]}")
