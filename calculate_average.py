import pandas as pd

# Load the updated CSV file
file_path = 'results2.csv'  # Update this with your actual file path
df = pd.read_csv(file_path)

# Clean column names by stripping spaces
df.columns = df.columns.str.strip()

# Filter for valid search methods (dfs, bfs, ucs) and exclude rows where the result is "ERROR"
df_filtered = df[(df['Search Method'].isin(['depthFirstSearch', 'breadthFirstSearch', 'uniformCostSearch'])) & (df['Solution State'] != 'ERROR')]

# Convert columns to numeric, coercing errors to NaN
df_filtered['Solution Depth'] = pd.to_numeric(df_filtered['Solution Depth'], errors='coerce')
df_filtered['Nodes Expanded'] = pd.to_numeric(df_filtered['Nodes Expanded'], errors='coerce')
df_filtered['Max Fringe Size'] = pd.to_numeric(df_filtered['Max Fringe Size'], errors='coerce')
df_filtered['Branching Factor'] = pd.to_numeric(df_filtered['Branching Factor'], errors='coerce')

# Remove rows with NaN values in any of the relevant columns
df_filtered = df_filtered.dropna(subset=['Solution Depth', 'Nodes Expanded', 'Max Fringe Size', 'Branching Factor'])

# Group by search method and calculate the averages, rounding to 2 decimal places
grouped_df = df_filtered.groupby('Search Method').agg(
    Average_Depth=('Solution Depth', 'mean'),
    Average_Nodes_Expanded=('Nodes Expanded', 'mean'),
    Average_Fring_Size=('Max Fringe Size', 'mean'),
    Average_Branching_Factor=('Branching Factor', 'mean')
).round(2).reset_index()

# Save the results to a new CSV file
output_file_path = 'average_results_per_search_method.csv'
grouped_df.to_csv(output_file_path, index=False)

print(f"Averages calculated and saved to {output_file_path}")
