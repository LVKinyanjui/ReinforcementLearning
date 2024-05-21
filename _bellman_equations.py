import numpy as np

class BellmanEquation:

    def __init__(self, rows=5, columns=5) -> None:
        
        # Initialize state space
        self.state_space = np.random.rand(rows, columns)
        
    def evaluate(self) -> None:
        self.state_space
