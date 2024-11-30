import pandas as pd
import math

# Load the CSV file
file_path = 'results2.csv'  # Update this with your actual file path
df = pd.read_csv(file_path)

# Define the branching factor function
def branching_factor(depth, num_expanded_nodes):
    if depth <= 0 or num_expanded_nodes <= 0:
        return -1  # Preserve -1 for invalid data
    b = round(math.pow(num_expanded_nodes, (1 / depth)), 3)
    return b

# Clean column names by stripping spaces
df.columns = df.columns.str.strip()

# Apply the branching factor function to all rows
df['Branching Factor'] = df.apply(
    lambda row: branching_factor(row['Depth'], row['Nodes Expanded']),
    axis=1
)

# Save the updated DataFrame to a new CSV file
output_file_path = 'updated_results.csv'
df.to_csv(output_file_path, index=False)

print(f"Branching factor calculated and saved to {output_file_path}")
