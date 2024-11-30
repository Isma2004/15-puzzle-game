# 15-puzzle-game
15-Puzzle Solver with Search Heuristics

This repository contains a project for solving the 15-puzzle game using various search heuristics and algorithms. The project demonstrates the application of artificial intelligence techniques to optimize search strategies and evaluate heuristic performance.

Features

	•	Implementation of a 15-puzzle solver with admissible heuristics.
	•	Comparison of heuristic performance (depth of solution, expanded nodes, max fringe size, execution time).
	•	Automatic generation and testing of initial puzzle states.
	•	Comparison of heuristic-based search with other strategies (BFS, DFS, etc.).

How It Works

	1.	15-Puzzle Implementation:
	•	Adapted the existing 8-puzzle logic to handle the 15-puzzle.
	•	Ensured the blank space ends in the bottom-right corner.
	2.	Search Heuristics:
	•	Implemented admissible heuristics (h1, h2, h3, h4).
	•	Compared heuristics based on solution metrics (depth, nodes expanded, max fringe size).
	3.	Automated Testing:
	•	Generated and tested random initial states using scenarios.csv.
	•	Compared heuristic performance and determined the best-performing strategy.
	4.	Comparison with Other Strategies:
	•	Benchmarked the best heuristic against BFS, DFS, and other strategies.

Results

	•	Identified the most efficient heuristic based on average metrics.
	•	Provided an overall comparison of heuristic and non-heuristic strategies.
