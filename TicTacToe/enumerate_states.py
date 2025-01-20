from collections import deque

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

def count_states():
    states = set()
    initial = tuple(tuple('.' * 3) for _ in range(3))
    queue = deque([(initial, 'X')])  # X goes first
    
    while queue:
        board, player = queue.pop()
        board_str = ''.join(''.join(row) for row in board)
        if board_str in states:
            continue
        states.add(board_str)
        
        # If current board is a winning state, don't add more moves
        if is_winner(board, 'X') or is_winner(board, 'O'):
            continue
            
        # Try each empty cell
        for i in range(3):
            for j in range(3):
                if board[i][j] == '.':
                    new_board = list(list(row) for row in board)
                    new_board[i][j] = player
                    new_board = tuple(tuple(row) for row in new_board)
                    queue.appendleft((new_board, 'O' if player == 'X' else 'X'))
    
    return len(states)

print(f"Total number of legal tic-tac-toe states: {count_states()}")
