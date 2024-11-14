import pandas as pd
import numpy as np

# Read the Excel file
df = pd.read_excel("connection_molecule_without_selfmel.xlsx", header=None)  # Assuming no header in the file

# Group by the second column and aggregate the first column values
grouped = df.groupby(1)[0].apply(list).reset_index()

# Find the maximum length of the lists
max_length = grouped[0].apply(len).max()

# Pad the lists with NaN values to make them equal in length
for index, row in grouped.iterrows():
    number = row[1]
    values = row[0]
    grouped.at[index, 0] = [number] + values + [np.nan] * (max_length - len(values))

# Create a new DataFrame to hold the result
result_df = pd.DataFrame()

# Iterate through the grouped data and add the lists to the result DataFrame
for index, row in grouped.iterrows():
    number = row[1]
    values = row[0]
    result_df[number] = values

# Transpose the result DataFrame
result_df = result_df.transpose()

# Write the result to a new Excel file
result_df.to_excel("mel_acr_junctions.xlsx", index=False, header=False)
