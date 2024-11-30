import pandas as pd

# Load the updated CSV file
file_path = 'updated_results.csv'  # Update this with your actual file path
df = pd.read_csv(file_path)

# Clean column names by stripping spaces
df.columns = df.columns.str.strip()

# Filter for valid search methods (dfs, bfs, ucs)
df_filtered = df[df['Solved'].isin(['depthFirstSearch', 'breadthFirstSearch', 'uniformCostSearch'])]

# Group by search method and calculate the averages
grouped_df = df_filtered.groupby('Solved').agg(
    Average_Depth=('Depth', 'mean'),
    Average_Nodes_Expanded=('Nodes Expanded', 'mean'),
    Average_Fring_Size=('Max Fringe Size', 'mean'),
    Average_Branching_Factor=('Branching Factor', 'mean')
).reset_index()

# Save the results to a new CSV file
output_file_path = 'average_results_per_search_method.csv'
grouped_df.to_csv(output_file_path, index=False)

print(f"Averages calculated and saved to {output_file_path}")
