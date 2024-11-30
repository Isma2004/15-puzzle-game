import csv
import time
from fifteenpuzzle import fifteen_Puzzle_State, FifteenPuzzleSearchProblem
from search import aStarSearch, h1, h2, h3, h4, h5


def read_scenarios(file_path):
    configurations = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            configuration = list(map(int, row))
            if len(configuration) == 16 and 0 in configuration:
                configurations.append(configuration)
            else:
                print(f"Skipping invalid configuration: {configuration}")
    return configurations


def check_if_solvable(puzzle):
    """Check if a 15-puzzle is solvable."""
    if 0 not in puzzle:
        raise ValueError(f"Invalid puzzle configuration: {puzzle} (missing blank tile '0')")

    inversions = 0
    for i in range(len(puzzle)):
        for j in range(i + 1, len(puzzle)):
            if puzzle[i] != 0 and puzzle[j] != 0 and puzzle[i] > puzzle[j]:
                inversions += 1

    # Find the row of the blank (0) from the bottom
    blank_row = 4 - (puzzle.index(0) // 4)  # 1-based row number from the bottom

    # Check solvability based on inversions and blank row position
    if blank_row % 2 == 0:  # Blank is on an even row from the bottom
        return inversions % 2 == 1
    else:  # Blank is on an odd row from the bottom
        return inversions % 2 == 0


def solve_puzzles(configurations, heuristics):
    results = []
    for i, config in enumerate(configurations):
        print(f"Solving puzzle {i + 1}/{len(configurations)} with configuration: {config}")

        if not check_if_solvable(config):
            print(f"Puzzle {config} is unsolvable. Skipping...")
            continue  # Skip unsolvable puzzles
        temp = f"{config}"
        print(temp)
        puzzle_state = fifteen_Puzzle_State(config)
        problem = FifteenPuzzleSearchProblem(puzzle_state)
        for heuristic in heuristics:
            print(f"Using heuristic: {heuristic.__name__}")
            start_time = time.time()

            # Ensure aStarSearch is properly returning results
            actions, nodes_expanded, max_fringe, bf = aStarSearch(problem, heuristic)
            elapsed_time = time.time() - start_time

            if actions is None or len(actions) == 0:  # Check for both None and empty list
                results.append([temp, heuristic.__name__, "Unsolved", -1, nodes_expanded, max_fringe, bf])
            else:
                solution_depth = len(actions)
                results.append([temp, heuristic.__name__, "Solved", solution_depth, nodes_expanded, max_fringe, bf])

            print(
                f"Heuristic {heuristic.__name__} finished. Nodes expanded: {nodes_expanded}, Time: {elapsed_time:.4f} seconds")

    return results


def write_results_to_csv(results, filename):
    """Write the results to a CSV file with a structured and readable format."""
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write the header with fixed widths
        header = ["Configuration", "Heuristic", "Solved", "Solution Depth", "Nodes Expanded", "Max Fringe Size", "Branching Factor"]
        writer.writerow(header)

        # Create a structured table format with padding for each column
        for result in results:
            configuration_str = ', '.join(map(str, result[0]))  # Convert the configuration list to a string

            # Make the row data more structured
            row_data = [
                result[0],  # Configuration
                result[1].ljust(8),        # Heuristic
                result[2].ljust(7),        # Solved
                str(result[3]).rjust(14),  # Solution Depth
                str(result[4]).rjust(14),  # Nodes Expanded
                str(result[5]).rjust(16), # Max Fringe Size
                str(result[6]).rjust(16), # Branching Factor
            ]

            writer.writerow(row_data)

    print(f"Results written to {filename} successfully.")


def main():
    HEURISTICS = [h1, h2, h3, h4,h5]

    # Read the puzzle configurations from the CSV file
    configurations = read_scenarios('Scenario.csv')
    print(configurations)
    write_results_to_csv(solve_puzzles(configurations, HEURISTICS), "results.csv")


if __name__ == "__main__":
    main()
