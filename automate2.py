import csv
import time
from fifteenpuzzle import fifteen_Puzzle_State, FifteenPuzzleSearchProblem
from search import depthFirstSearch, breadthFirstSearch, uniformCostSearch


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


def write_results_to_csv(results, filename):
    """Write the results to a CSV file with a structured and readable format."""
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write the header with fixed widths
        header = ["Configuration", "Search Method", "Solution State","Solution Depth",
                  "Nodes Expanded", "Max Fringe Size", "Branching Factor"]
        writer.writerow(header)

        # Create a structured table format with padding for each column
        for result in results:
            # Convert the configuration list to a string
            configuration_str = ', '.join(map(str, result[0]))

            # Make the row data more structured
            row_data = [
                result[0],  # Configuration
                result[1].ljust(8),  # Uninformed search method
                result[2].ljust(7),  # Solved
                str(result[3]).rjust(14),  # Solution Depth
                str(result[4]).rjust(14),  # Nodes Expanded
                str(result[5]).rjust(16),  # Max Fringe Size
                str(result[6]).rjust(16),  # Branching Factor
            ]

            writer.writerow(row_data)

    print(f"Results written to {filename} successfully.")


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
    # 1-based row number from the bottom
    blank_row = 4 - (puzzle.index(0) // 4)

    # Check solvability based on inversions and blank row position
    if blank_row % 2 == 0:  # Blank is on an even row from the bottom
        return inversions % 2 == 1
    else:  # Blank is on an odd row from the bottom
        return inversions % 2 == 0


def solve_puzzles(configurations, search_methods):
    results = []
    for i, config in enumerate(configurations):
        print(f"Solving puzzle {i + 1}/{len(configurations)} with configuration: {config}")
        temp = f"{config}"

        if not check_if_solvable(config):
            print(f"Puzzle {config} is unsolvable. Skipping...")
            continue

        puzzle_state = fifteen_Puzzle_State(config)
        problem = FifteenPuzzleSearchProblem(puzzle_state)

        for search_method in search_methods:
            print(f"Using search method: {search_method.__name__}")
            start_time = time.time()

            # Adapt to the method's return values
            result = search_method(problem)
            elapsed_time = time.time() - start_time

            if result is None or len(result) == 0:
                results.append([temp, search_method.__name__,
                                "Unsolved", -1, -1, -1, -1])
            else:
                # BFS, DFS may not return these, modify as necessary based on the return
                depth, explored_nodes, max_fringe, bf = result if len(
                    result) == 4 else (len(result), -1, -1, -1)
                results.append([temp, search_method.__name__,
                                "Solved", depth, explored_nodes, max_fringe, bf])

            print(f"Search method {search_method.__name__} finished. Time: {elapsed_time:.4f} seconds")

    return results


def main():
    SEARCH_METHODS = [depthFirstSearch, breadthFirstSearch, uniformCostSearch]

    # Read the puzzle configurations from the CSV file
    configurations = read_scenarios('Scenario.csv')
    print(configurations)
    write_results_to_csv(solve_puzzles(
        configurations, SEARCH_METHODS), "results2.csv")


if __name__ == "__main__":
    main()
