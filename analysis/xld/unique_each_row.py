import pandas as pd

# Read the Excel file
df = pd.read_excel('mel_acr_junctions.xlsx', header=None)

# Define a function to extract unique numbers from each row while preserving the order
def extract_unique(row):
    unique_numbers = []
    seen_numbers = set()
    for num in row:
        if num not in seen_numbers:
            unique_numbers.append(num)
            seen_numbers.add(num)
    return unique_numbers

# Apply the function to each row
df['Unique Numbers'] = df.apply(extract_unique, axis=1)

# Write the result to a new Excel file
df['Unique Numbers'].apply(lambda x: pd.Series(x)).to_excel('unique_mel_acr_junctions_without_selfmel.xlsx', index=False, header=False)
