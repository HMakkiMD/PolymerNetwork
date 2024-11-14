import pandas as pd

# Replace with your file path
excel_file_path = 'selected_rows.xlsx'

try:
    df = pd.read_excel(excel_file_path)

    # Filter rows based on criteria using column names
    filtered_df = df[
        (df[1] >= 301) & (df[1] <= 1140) &
        (df['1.1'] >= 301) & (df['1.1'] <= 1140)
    ]

    if not filtered_df.empty:
        # Save the filtered data to a new Excel file
        output_file_path = 'filtered_excel_file.xlsx'  # Replace with output file path
        filtered_df.to_excel(output_file_path, index=False)
        print("Filtered data saved to", output_file_path)
    else:
        print("No rows found that meet the criteria.")

except FileNotFoundError:
    print("The specified file was not found.")
except Exception as e:
    print("An error occurred:", e)

# Load the Excel file
input_file = 'filtered_excel_file.xlsx'
output_file = 'mel-mel.xlsx'

# Read the Excel file into a pandas DataFrame
df = pd.read_excel(input_file)

# Identify column names
columns = df.columns

# Assuming the first and second columns are 'Column1' and 'Column2'
# Change these column names accordingly
column1_name = columns[0]
column2_name = columns[1]

# Filter rows where the values in 'Column1' and 'Column2' are not equal
filtered_df = df[df[column1_name] != df[column2_name]]

# Write the filtered DataFrame to a new Excel file
filtered_df.to_excel(output_file, index=False)

# Find duplicate rows in the output Excel file
output_df = pd.read_excel(output_file)
duplicate_rows = output_df[output_df.duplicated()]

# Count the number of duplicate rows
num_duplicates = len(duplicate_rows)
print(duplicate_rows)
print(f"Number of duplicate rows in the output Excel file: {num_duplicates}")
df = pd.read_excel('mel-mel.xlsx')
length_of_data = len(df)
print("Length of data in mel-mel.xlsx:", length_of_data)
# Save the numbers to an existing Excel file "analysis.xlsx" in a new sheet
existing_file = 'analysis.xlsx'
with pd.ExcelWriter(existing_file, mode='a', engine='openpyxl') as writer:
    # Write filtered data to a new sheet
    filtered_df.to_excel(writer, sheet_name='mel-mel', index=False)
    
    # Write num_duplicates to cell D1
    workbook = writer.book
    worksheet = writer.sheets['mel-mel']
    worksheet['D1'] = num_duplicates
    worksheet['C1'] = length_of_data


