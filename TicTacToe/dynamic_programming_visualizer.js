import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { RefreshCw, ArrowLeft } from 'lucide-react';

// Value iteration implementation (same as before)
const boardToString = (board) => board.flat().join('');

const isWinner = (board, player) => {
  // Check rows, columns, and diagonals
  for (let i = 0; i < 3; i++) {
    if (board[i].every(cell => cell === player) ||
        board.every(row => row[i] === player)) {
      return true;
    }
  }
  if (board.every((row, i) => row[i] === player) ||
      board.every((row, i) => row[2-i] === player)) {
    return true;
  }
  return false;
};

const getNextStates = (board, player) => {
  const states = [];
  board.forEach((row, i) => {
    row.forEach((cell, j) => {
      if (cell === '.') {
        const newBoard = board.map(row => [...row]);
        newBoard[i][j] = player;
        states.push(newBoard);
      }
    });
  });
  return states;
};

const valueIteration = (epsilon = 0.0001) => {
  const V = new Map();
  const initial = Array(3).fill().map(() => Array(3).fill('.'));
  const queue = [[initial, 'X']];
  
  // First pass: enumerate states and set terminal values
  while (queue.length > 0) {
    const [board, player] = queue.pop();
    const boardStr = boardToString(board);
    if (V.has(boardStr)) continue;
    
    if (isWinner(board, 'X')) V.set(boardStr, 1.0);
    else if (isWinner(board, 'O')) V.set(boardStr, -1.0);
    else if (!boardStr.includes('.')) V.set(boardStr, 0.0);
    else {
      V.set(boardStr, 0.0);
      const nextPlayer = player === 'X' ? 'O' : 'X';
      getNextStates(board, player).forEach(nextBoard => {
        queue.unshift([nextBoard, nextPlayer]);
      });
    }
  }
  
  // Value iteration
  let delta = Infinity;
  while (delta > epsilon) {
    delta = 0;
    for (const [boardStr] of V) {
      const board = Array(3).fill().map((_, i) => 
        Array(3).fill().map((_, j) => boardStr[i * 3 + j])
      );
      const oldV = V.get(boardStr);
      
      if (isWinner(board, 'X') || isWinner(board, 'O') || !boardStr.includes('.')) 
        continue;
      
      const xCount = boardStr.split('X').length - 1;
      const oCount = boardStr.split('O').length - 1;
      const player = xCount === oCount ? 'X' : 'O';
      
      const nextValues = getNextStates(board, player)
        .map(s => V.get(boardToString(s)));
      
      if (nextValues.length > 0) {
        V.set(boardStr, player === 'X' ? Math.max(...nextValues) : Math.min(...nextValues));
        delta = Math.max(delta, Math.abs(oldV - V.get(boardStr)));
      }
    }
  }
  
  return V;
};

const TicTacToeVisualizer = () => {
  const [history, setHistory] = useState([Array(3).fill().map(() => Array(3).fill('.'))]);
  const [currentMove, setCurrentMove] = useState(0);
  const V = React.useMemo(() => valueIteration(), []);
  
  const currentBoard = history[currentMove];
  const xIsNext = currentMove % 2 === 0;
  const currentPlayer = xIsNext ? 'X' : 'O';
  
  const getNextMoves = () => {
    const moves = [];
    currentBoard.forEach((row, i) => {
      row.forEach((cell, j) => {
        if (cell === '.') {
          const newBoard = currentBoard.map(row => [...row]);
          newBoard[i][j] = currentPlayer;
          const value = V.get(boardToString(newBoard));
          moves.push({ i, j, value });
        }
      });
    });
    return moves;
  };

  const handleClick = (i, j) => {
    if (currentBoard[i][j] !== '.' || isWinner(currentBoard, 'X') || isWinner(currentBoard, 'O')) 
      return;
      
    const newHistory = history.slice(0, currentMove + 1);
    const newBoard = currentBoard.map(row => [...row]);
    newBoard[i][j] = currentPlayer;
    
    setHistory([...newHistory, newBoard]);
    setCurrentMove(currentMove + 1);
  };

  const reset = () => {
    setHistory([Array(3).fill().map(() => Array(3).fill('.'))]);
    setCurrentMove(0);
  };

  const undo = () => {
    if (currentMove > 0) {
      setCurrentMove(currentMove - 1);
    }
  };

  const getBgColor = (value) => {
    if (value === undefined) return 'bg-gray-100';
    const intensity = Math.abs(value) * 200;
    return value > 0 
      ? `rgb(${255-intensity}, 255, ${255-intensity})` 
      : `rgb(255, ${255-intensity}, ${255-intensity})`;
  };

  const nextMoves = getNextMoves();
  const boardValue = V.get(boardToString(currentBoard));

  return (
    <Card className="w-full max-w-xl mx-auto">
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span>Tic Tac Toe Value Function</span>
          <div className="space-x-2">
            <Button variant="outline" size="icon" onClick={undo} disabled={currentMove === 0}>
              <ArrowLeft className="h-4 w-4" />
            </Button>
            <Button variant="outline" size="icon" onClick={reset}>
              <RefreshCw className="h-4 w-4" />
            </Button>
          </div>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="mb-4 text-center">
          Current Position Value: {boardValue?.toFixed(3) || 'N/A'}
          {boardValue === 1 && " (X wins)"}
          {boardValue === -1 && " (O wins)"}
          {boardValue === 0 && " (Draw)"}
        </div>
        <div className="grid grid-cols-3 gap-2 w-full max-w-sm mx-auto mb-4">
          {currentBoard.map((row, i) => (
            row.map((cell, j) => {
              const move = nextMoves.find(m => m.i === i && m.j === j);
              return (
                <button
                  key={`${i}-${j}`}
                  className="aspect-square flex items-center justify-center text-2xl font-bold border rounded"
                  style={{ backgroundColor: getBgColor(move?.value) }}
                  onClick={() => handleClick(i, j)}
                >
                  {cell === '.' ? (
                    move ? <span className="text-sm text-gray-500">
                      {move.value.toFixed(2)}
                    </span> : ''
                  ) : cell}
                </button>
              )
            })
          ))}
        </div>
        <div className="text-center">
          {isWinner(currentBoard, 'X') ? "X Wins!" :
           isWinner(currentBoard, 'O') ? "O Wins!" :
           !currentBoard.flat().includes('.') ? "Draw!" :
           `Next player: ${currentPlayer}`}
        </div>
      </CardContent>
    </Card>
  );
};

export default TicTacToeVisualizer;
