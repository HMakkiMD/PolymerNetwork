import pandas as pd

# Read the Excel file into a DataFrame
df = pd.read_excel('selected_rows.xlsx')

# Filter rows where the first and second columns are different
df = df[df.iloc[:, 0] != df.iloc[:, 1]]

# Write the modified DataFrame back to an Excel file
df.to_excel('connection_molecule.xlsx', index=False)
