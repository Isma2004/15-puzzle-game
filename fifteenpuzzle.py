# fifteenpuzzle.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
import random

import search
import util


# Module Classes
# /=====Start Change Task i=====/------------------------------------------------------------------------------------
class fifteen_Puzzle_State:

    def __init__(self, numbers):
        # Ensure the input contains 16 elements
        if len(numbers) != 16:
            raise ValueError("The puzzle must contain exactly 16 elements.")

        self.cells = []
        self.blankLocation = None  # This will store the position of the blank (0) tile

        for row in range(4):
            self.cells.append([])
            for col in range(4):
                value = numbers.pop(0)  # Get the next tile value
                self.cells[row].append(value)
                if value == 0:
                    self.blankLocation = (row, col)  # Store the blank's position

        if self.blankLocation is None:
            raise ValueError("Puzzle must contain a blank tile represented by 0.")

    # /=====End Change# Task i =====/

    # /=====Start Change Task i=====/

    def isGoal(self):
        """
        Checks if the puzzle is in the goal state.
        """
        goal = list(range(1, 16)) + [0]  # The goal state (flattened)
        flat_cells = sum(self.cells, [])  # Flatten the 2D grid into a 1D list
        return flat_cells == goal

    # /=====End Change Task i=====/----------------------------------------------------------------------------------

    # /=====start Change Task i=====/--------------------------------------------------------------------------------
    def legalMoves(self):
        row, col = self.blankLocation  # Get the current position of the blank tile
        moves = []

        if row > 0:  # Can move the blank up
            moves.append('up')
        if row < 3:  # Can move the blank down
            moves.append('down')
        if col > 0:  # Can move the blank left
            moves.append('left')
        if col < 3:  # Can move the blank right
            moves.append('right')

        return moves # Return the list of valid moves based on the blank tile's position

    # /=====End Change Task i=====/--------------------------------------------------------------------------------

    # /=====start Change Task i=====/--------------------------------------------------------------------------------
    def result(self, move):
        """
        Applies the given move ('up', 'down', 'left', 'right') and returns the new state.
        """
        row, col = self.blankLocation

        if move == 'up':
            new_row, new_col = row - 1, col
        elif move == 'down':
            new_row, new_col = row + 1, col
        elif move == 'left':
            new_row, new_col = row, col - 1
        elif move == 'right':
            new_row, new_col = row, col + 1
        else:
            raise ValueError(f"Illegal move: {move}")

        # Create a new puzzle state and update it with the move
        new_puzzle = fifteen_Puzzle_State([0] * 16)
        new_puzzle.cells = [row.copy() for row in self.cells]  # Use a faster copying method
        new_puzzle.cells[row][col], new_puzzle.cells[new_row][new_col] = (
            new_puzzle.cells[new_row][new_col],
            new_puzzle.cells[row][col],
        )
        new_puzzle.blankLocation = (new_row, new_col)

        return new_puzzle

    # /=====End Change Task i=====/--------------------------------------------------------------------------------

    # Utilities for comparison and display

    # /=====start Change Task i=====/--------------------------------------------------------------------------------
    def __eq__(self, other):
        if isinstance(other, fifteen_Puzzle_State):
            return self.cells == other.cells
        return False

    def __hash__(self):
        return hash(tuple(map(tuple, self.cells)))

    def __getAsciiString(self):
        """
        Returns a display string for the 15-puzzle.
        """
        lines = []
        horizontalLine = ('-' * 17)  # Adjust the horizontal line for the 4x4 grid
        lines.append(horizontalLine)

        # Loop over the 4x4 grid to print each row
        for row in self.cells:
            rowLine = '|'
            for col in row:
                if col == 0:
                    col = ' '  # Display a space for the blank tile
                rowLine += ' ' + str(col).rjust(2) + ' |'  # Adjust spacing for double-digit numbers
            lines.append(rowLine)
            lines.append(horizontalLine)

        return '\n'.join(lines)  # Join the lines into a string with newlines in between

    def __str__(self):
        """
        Returns a human-readable string representation of the puzzle using __getAsciiString.
        """
        return self.__getAsciiString()

    def __lt__(self, other):
        """
        Compares two puzzle states for priority queue.
        We use tuple representation of the state for faster comparison.
        """
        return tuple(map(tuple, self.cells)) < tuple(map(tuple, other.cells))


# /=====End Change Task i=====/--------------------------------------------------------------------------------------

# TODO: Implement The methods in this class
# /=====Start Change Task i=====/--------------------------------------------------------------------------------
class FifteenPuzzleSearchProblem(search.SearchProblem):
    """
      Implementation of a SearchProblem for the  Eight Puzzle domain

      Each state is represented by an instance of an eightPuzzle.
    """

    def __init__(self, puzzle):
        """
        Initialize the search problem with the starting state of the puzzle.
        """
        self.puzzle = puzzle  # Store the initial puzzle state
        self.expanded_nodes = 0  # To track the number of expanded nodes
        self.max_fringe_size = 0  # To track the maximum size of the fringe

    def getStartState(self):
        """
        Returns the initial puzzle state.
        """
        return self.puzzle

    def isGoalState(self, state):
        """
        Returns True if the given state is the goal state.
        """
        return state.isGoal()

    def getSuccessors(self, state):
        """
        Returns a list of (successor, action, stepCost) tuples.
        Each successor is the result of a valid move from the current state.
        """
        successors = []

        for move in state.legalMoves():
            new_state = state.result(move)
            successors.append((new_state, move, 1))  # The step cost is 1 for every move

        return successors

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)


# /=====End Change Task i=====/--------------------------------------------------------------------------------

# /=====start * Change Task i=====/----------------------------------------------------------------------------

FIFTEEN_PUZZLE_DATA = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0],  # Goal state
    [1, 2, 3, 4, 5, 6, 0, 7, 9, 10, 8, 11, 13, 14, 12, 15],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 10, 11, 13, 14, 12, 15],
    [4, 1, 2, 3, 5, 6, 7, 0, 9, 10, 11, 8, 13, 14, 15, 12],
    [5, 1, 3, 4, 2, 6, 7, 8, 9, 10, 11, 0, 13, 14, 15, 12]
]


# /=====End Change Task i=====/
def loadEightPuzzle(puzzleNumber):
    """
    puzzleNumber: The number of the 15-puzzle to load.

    Returns a 15-puzzle object generated from one of the
    provided puzzles in FIFTEEN_PUZZLE_DATA.

    puzzleNumber can range from 0 to 4.
    """
    return fifteen_Puzzle_State(FIFTEEN_PUZZLE_DATA[puzzleNumber])


def createRandomFifteenPuzzle(moves=100):
    """
    moves: number of random moves to apply

    Creates a random 15-puzzle by applying a series of 'moves' random moves to a solved puzzle.
    """
    puzzle = fifteen_Puzzle_State([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0])  # Start with the goal state
    for i in range(moves):
        # Execute a random legal move
        puzzle = puzzle.result(random.sample(puzzle.legalMoves(), 1)[0])
    return puzzle


if __name__ == '__main__':
    puzzle = createRandomFifteenPuzzle(25)  # Generate a random 15-puzzle with 25 random moves
    print('A random puzzle:')
    print(puzzle)  # Display the puzzle using the __str__ method

    # Use the FifteenPuzzleSearchProblem class
    problem = FifteenPuzzleSearchProblem(puzzle)
    path, nodes_expanded, _, max_fringe_size = search.aStarSearch(problem, search.h1)

    if path is None:
        print("No solution found.")
    else:
        print(f"A* found a path of {len(path)} moves: {path}")
        print(f"Nodes expanded: {nodes_expanded}, Maximum fringe size: {max_fringe_size}")

        curr = puzzle
        for i, a in enumerate(path, 1):
            curr = curr.result(a)  # Apply the move and get the new puzzle state
            print(f'After {i} move{"s" if i > 1 else ""}: {a}')
            print(curr)  # Print the new puzzle state using the __str__ method
            input("Press return for the next state...")

# /=====End Change Task i=====/--------------------------------------------------------------------------------
