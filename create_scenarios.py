# puzzle_utils.py
import random
import csv

def create_random_fifteen_puzzle(moves= 10):
    from copy import deepcopy

    solved_state = [list(range(1, 5)), list(range(5, 9)), list(range(9, 13)), list(range(13, 16)) + [0]]
    puzzle = deepcopy(solved_state)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
    last_pos = (3, 3)  # starting with the blank space in the bottom-right corner

    for _ in range(moves):
        while True:
            direction = random.choice(directions)
            new_pos = (last_pos[0] + direction[0], last_pos[1] + direction[1])
            if 0 <= new_pos[0] < 4 and 0 <= new_pos[1] < 4:
                puzzle[last_pos[0]][last_pos[1]], puzzle[new_pos[0]][new_pos[1]] = puzzle[new_pos[0]][new_pos[1]], puzzle[last_pos[0]][last_pos[1]]
                last_pos = new_pos
                break
    return puzzle

def save_puzzles_to_csv(filename, num_puzzles, moves_per_puzzle):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for _ in range(num_puzzles):
            puzzle = create_random_fifteen_puzzle(moves_per_puzzle)
            writer.writerow(sum(puzzle, []))  # Flatten and write the puzzle configuration

# Usage example to generate and save puzzles
if __name__ == "__main__":
    save_puzzles_to_csv('Scenario.csv', 1000, 10)