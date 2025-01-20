import random
import numpy as np
from collections import defaultdict

class TicTacToeQLearning:
    def __init__(self, alpha=0.1, epsilon=0.1, gamma=0.9):
        self.alpha = alpha      # Learning rate
        self.epsilon = epsilon  # Exploration rate
        self.gamma = gamma      # Discount factor
        self.Q = defaultdict(lambda: defaultdict(lambda: 0.0))  # Q-table
        
    def board_to_string(self, board):
        return ''.join(''.join(row) for row in board)
    
    def get_valid_actions(self, board):
        actions = []
        for i in range(3):
            for j in range(3):
                if board[i][j] == '.':
                    actions.append((i, j))
        return actions
    
    def is_winner(self, board, player):
        # Check rows, columns, and diagonals
        for i in range(3):
            if all(board[i][j] == player for j in range(3)) or \
               all(board[j][i] == player for j in range(3)):
                return True
        if all(board[i][i] == player for i in range(3)) or \
           all(board[i][2-i] == player for i in range(3)):
            return True
        return False
    
    def get_reward(self, board, player):
        if self.is_winner(board, player):
            return 1.0
        elif self.is_winner(board, 'O' if player == 'X' else 'X'):
            return -1.0
        elif not any('.' in row for row in board):  # Draw
            return 0.0
        return None  # Game not finished
    
    def choose_action(self, board, player):
        state = self.board_to_string(board)
        valid_actions = self.get_valid_actions(board)
        
        if random.random() < self.epsilon:  # Exploration
            return random.choice(valid_actions)
        
        # Exploitation (with some randomization of equal values)
        q_values = [self.Q[state][action] for action in valid_actions]
        max_q = max(q_values)
        best_actions = [action for action, q in zip(valid_actions, q_values) if q == max_q]
        return random.choice(best_actions)
    
    def make_move(self, board, action, player):
        new_board = [list(row) for row in board]
        new_board[action[0]][action[1]] = player
        return tuple(tuple(row) for row in new_board)
    
    def train(self, n_episodes=10000):
        for episode in range(n_episodes):
            board = tuple(tuple('.' * 3) for _ in range(3))
            player = 'X'
            
            while True:
                state = self.board_to_string(board)
                action = self.choose_action(board, player)
                
                # Make move and get new state
                new_board = self.make_move(board, action, player)
                reward = self.get_reward(new_board, player)
                
                if reward is not None:  # Terminal state
                    self.Q[state][action] += self.alpha * (reward - self.Q[state][action])
                    break
                
                # Get next state's max Q-value
                next_state = self.board_to_string(new_board)
                next_actions = self.get_valid_actions(new_board)
                next_max_q = max(self.Q[next_state][a] for a in next_actions)
                
                # Update Q-value
                self.Q[state][action] += self.alpha * (self.gamma * next_max_q - self.Q[state][action])
                
                board = new_board
                player = 'O' if player == 'X' else 'X'
            
            # Decay epsilon
            self.epsilon = max(0.01, self.epsilon * 0.9999)

    def get_best_move(self, board):
        state = self.board_to_string(board)
        valid_actions = self.get_valid_actions(board)
        q_values = [self.Q[state][action] for action in valid_actions]
        max_q = max(q_values)
        return random.choice([action for action, q in zip(valid_actions, q_values) if q == max_q])

# Training and demonstration
agent = TicTacToeQLearning()
agent.train(n_episodes=50000)

# Print Q-values for initial state
initial_board = tuple(tuple('.' * 3) for _ in range(3))
state = agent.board_to_string(initial_board)
print("\nLearned Q-values for initial state:")
for action in agent.get_valid_actions(initial_board):
    print(f"Move {action}: {agent.Q[state][action]:.3f}")
