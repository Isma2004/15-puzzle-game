# search.py
# ---------
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


"""
In search.py, we implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""
import math

import util
from math import sqrt
from queue import PriorityQueue


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def branching_factor(depth, num_expandedNodes):
    if (depth == 0):
        return 'ERROR'
    b = round(math.pow(num_expandedNodes, (1 / depth)), 3)

    return b


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


import util


def depthFirstSearch(problem, maxDepth=25):
    """Search the deepest nodes in the search tree first, constrained by max depth."""

    # Stack to hold nodes in the form (state, actions leading to the state, current depth)
    frontier = util.Stack()
    # Set to keep track of explored nodes
    exploredNodes = set()
    max_fringe_size = 0
    current_fringe_size = 0

    # Get the start state of the problem
    startState = problem.getStartState()
    # Start node (state, actions, current depth)
    startNode = (startState, [], 0)

    # Push the start node to the frontier
    frontier.push(startNode)
    current_fringe_size += 1  # Increase fringe size when a new node is added

    # Continue exploring until the frontier is empty
    while not frontier.isEmpty():
        # Pop the most recent node from the frontier
        currentState, actions, depth = frontier.pop()
        current_fringe_size -= 1  # Decrease fringe size when a node is removed
        depth = max(depth, len(actions))
        # If the current depth exceeds the maximum depth, skip this node
        if depth > maxDepth:
            continue

        # If the current state hasn't been explored
        if currentState not in exploredNodes:
            # Mark the current state as explored
            exploredNodes.add(currentState)

            # If the current state is the goal, return the actions leading to it
            if problem.isGoalState(currentState):
                bf = branching_factor(depth, len(exploredNodes))
                return depth, len(exploredNodes), max_fringe_size, bf

            # Get successors of the current state (successor, action, cost)
            successors = problem.getSuccessors(currentState)

            # Add successors to the frontier if they haven't been explored
            for succState, succAction, succCost in successors:
                if succState not in exploredNodes:
                    newAction = actions + [succAction]
                    newNode = (succState, newAction, depth + 1)
                    frontier.push(newNode)
                    current_fringe_size += 1  # Increase fringe size for each new successor added
                    max_fringe_size = max(max_fringe_size, current_fringe_size)

    # If no solution is found, print and return an empty list
    print(f"No solution was found due to reaching max depth: {maxDepth}.")
    return depth, len(exploredNodes), max_fringe_size, 0


import queue  # Built-in Python module


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    # To be explored (FIFO)
    frontier = queue.Queue()
    exploredNodes = set()  # Using a set for faster lookup
    max_fringe_size = 0

    # Get the start state of the problem
    startState = problem.getStartState()
    startNode = (startState, [], 0)  # (state, actions, cost)
    depth = 0

    # Push the start node to the frontier
    frontier.put(startNode)

    while not frontier.empty():
        # Begin exploring the first (earliest-pushed) node on frontier
        currentState, actions, currentCost = frontier.get()
        depth = max(depth, len(actions))
        if currentState not in exploredNodes:
            # Put popped node state into explored set
            exploredNodes.add(currentState)

            # Check if the current state is the goal
            if problem.isGoalState(currentState):
                bf = branching_factor(len(actions), len(exploredNodes))
                return len(actions), len(exploredNodes), max_fringe_size, bf

            else:
                # List of (successor, action, stepCost)
                successors = problem.getSuccessors(currentState)

                for succState, succAction, succCost in successors:
                    newAction = actions + [succAction]
                    newCost = currentCost + succCost
                    newNode = (succState, newAction, newCost)

                    # Add new node to the frontier if not already explored
                    if succState not in exploredNodes:
                        frontier.put(newNode)
                        # Update max fringe size using qsize()
                        max_fringe_size = max(max_fringe_size, frontier.qsize())

    return len(actions), len(exploredNodes), max_fringe_size, 0


def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    # to be explored (FIFO): holds (item, cost)
    frontier = util.PriorityQueue()
    depth = 0
    # previously expanded states (for cycle checking), holds state:cost
    exploredNodes = {}

    startState = problem.getStartState()
    startNode = (startState, [], 0)  # (state, action, cost)
    max_fringe_size = 0
    frontier.push(startNode, 0)

    while not frontier.isEmpty():
        # begin exploring first (lowest-cost) node on frontier
        currentState, actions, currentCost = frontier.pop()
        depth = max(depth, len(actions))
        if (currentState not in exploredNodes) or (currentCost < exploredNodes[currentState]):
            # put popped node's state into explored list
            exploredNodes[currentState] = currentCost

            if problem.isGoalState(currentState):
                bf = branching_factor(depth, len(exploredNodes))
                return depth, len(exploredNodes), max_fringe_size, bf
            else:
                # list of (successor, action, stepCost)
                successors = problem.getSuccessors(currentState)

                for succState, succAction, succCost in successors:
                    newAction = actions + [succAction]
                    newCost = currentCost + succCost
                    newNode = (succState, newAction, newCost)
                    max_fringe_size = max(max_fringe_size, len(frontier.heap))
                    frontier.update(newNode, newCost)

    return depth, len(exploredNodes), max_fringe_size, 0


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


from queue import PriorityQueue
from math import sqrt


def h1(state, problem=None):
    goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
    current_state = sum(state.cells, [])  # Flatten the 2D list
    return sum(1 for i in range(16) if current_state[i] != goal_state[i] and current_state[i] != 0)


def h2(state, problem=None):
    goal_position = {1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (0, 3),
                     5: (1, 0), 6: (1, 1), 7: (1, 2), 8: (1, 3),
                     9: (2, 0), 10: (2, 1), 11: (2, 2), 12: (2, 3),
                     13: (3, 0), 14: (3, 1), 15: (3, 2), 0: (3, 3)}

    return sum(
        sqrt((goal_position[state.cells[row][col]][0] - row) ** 2 +
             (goal_position[state.cells[row][col]][1] - col) ** 2)
        for row in range(4) for col in range(4) if state.cells[row][col] != 0
    )


def h3(state, problem=None):
    goal_position = {1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (0, 3),
                     5: (1, 0), 6: (1, 1), 7: (1, 2), 8: (1, 3),
                     9: (2, 0), 10: (2, 1), 11: (2, 2), 12: (2, 3),
                     13: (3, 0), 14: (3, 1), 15: (3, 2), 0: (3, 3)}

    return sum(
        abs(goal_position[state.cells[row][col]][0] - row) + abs(goal_position[state.cells[row][col]][1] - col)
        for row in range(4) for col in range(4) if state.cells[row][col] != 0
    )


def h4(state, problem=None):
    goal_position = {1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (0, 3),
                     5: (1, 0), 6: (1, 1), 7: (1, 2), 8: (1, 3),
                     9: (2, 0), 10: (2, 1), 11: (2, 2), 12: (2, 3),
                     13: (3, 0), 14: (3, 1), 15: (3, 2), 0: (3, 3)}

    out_of_row = sum(1 for row in range(4) for col in range(4)
                     if state.cells[row][col] != 0 and goal_position[state.cells[row][col]][0] != row)
    out_of_col = sum(1 for row in range(4) for col in range(4)
                     if state.cells[row][col] != 0 and goal_position[state.cells[row][col]][1] != col)

    return out_of_row + out_of_col


# this is a custom heuristic 5 that combines the h3 manhatan distance for the early stage of the problem and the h4
# with the out of row and column


def h5(state, problem=None):
    goal_position = {1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (0, 3),
                     5: (1, 0), 6: (1, 1), 7: (1, 2), 8: (1, 3),
                     9: (2, 0), 10: (2, 1), 11: (2, 2), 12: (2, 3),
                     13: (3, 0), 14: (3, 1), 15: (3, 2), 0: (3, 3)}

    # Manhattan distance (h3)
    manhattan_distance = sum(
        abs(goal_position[state.cells[row][col]][0] - row) + abs(goal_position[state.cells[row][col]][1] - col)
        for row in range(4) for col in range(4) if state.cells[row][col] != 0
    )

    # Out of row/column (h4)
    out_of_row = sum(1 for row in range(4) for col in range(4)
                     if state.cells[row][col] != 0 and goal_position[state.cells[row][col]][0] != row)
    out_of_col = sum(1 for row in range(4) for col in range(4)
                     if state.cells[row][col] != 0 and goal_position[state.cells[row][col]][1] != col)

    return manhattan_distance + (out_of_row + out_of_col)


def aStarSearch(problem, heuristic):
    frontier = util.PriorityQueue()
    fringe_size = 0
    depth = 0
    exploredNodes = set()  # Changed to set for O(1) lookup
    startState = problem.getStartState()
    startNode = (startState, [], 0)  # (state, action, cost)

    frontier.push(startNode, 0)
    # Track costs to reach states that have been seen
    seenStates = {startState: 0}

    while not frontier.isEmpty():
        currentState, actions, currentCost = frontier.pop()

        if currentState in exploredNodes:
            continue

        exploredNodes.add(currentState)
        fringe_size = max(frontier.count, fringe_size)
        if problem.isGoalState(currentState):
            bf = branching_factor(depth, len(exploredNodes))
            return actions, len(exploredNodes), fringe_size, bf

        for succState, succAction, succCost in problem.getSuccessors(currentState):
            newAction = actions + [succAction]
            depth = max(depth, len(actions))
            newCost = currentCost + succCost

            # Only process new state or better cost found
            if succState not in seenStates or newCost < seenStates[succState]:
                seenStates[succState] = newCost
                frontier.push((succState, newAction, newCost), newCost + heuristic(succState, problem))

    return [], len(exploredNodes), fringe_size, 0  # Return empty path if not found



