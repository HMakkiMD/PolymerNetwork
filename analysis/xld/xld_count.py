import pandas as pd

def count_rows_with_specific_columns(file_path, num_columns):
    try:
        # Read the Excel file
        df = pd.read_excel(file_path, header=None)
        
        # Count the rows with exactly the specified number of columns containing numbers
        count = sum(df.apply(lambda row: row.dropna().apply(lambda x: isinstance(x, (int, float))).sum() == num_columns, axis=1))
        
        return count
    except Exception as e:
        print("Error:", e)
        return None

# Example usage
file_path = 'unique_mel_acr_junctions_without_selfmel.xlsx'

output_file = "xld.txt"
total_sum = 0

with open(output_file, "w") as f:
    for num_columns in range(3, 8):
        num_rows = count_rows_with_specific_columns(file_path, num_columns)
        if num_rows is not None:
            total_sum += num_rows
            f.write(f"Number of melamine with {num_columns-1} junction to different acrylic: {num_rows}\n")
    
    f.write(f"Total melamine: {total_sum}")

print("Output written to", output_file)
