import pandas as pd

# Read the Excel file without header
df = pd.read_excel('connection_molecule.xlsx', header=None)

# Count the initial number of rows
initial_rows = len(df)

# Filter rows where both numbers in a row are larger than 300. This line must be changed based on system
df = df[(df.iloc[:, 0] <= 300) | (df.iloc[:, 1] <= 300)]

# Count the number of rows deleted
rows_deleted = initial_rows - len(df)

# Save the remaining data to a new Excel file
df.to_excel('connection_molecule_without_selfmel.xlsx', index=False, header=False)

# Print the number of rows deleted
print(f"Number of rows deleted: {rows_deleted}")
