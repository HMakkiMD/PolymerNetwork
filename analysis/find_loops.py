import pandas as pd

# Replace with your file path
excel_file_path = 'selected_rows.xlsx'

try:
    df = pd.read_excel(excel_file_path)

    # Filter rows based on criteria using column names
    filtered_df = df[
        (df[1] >= 1) & (df[1] <= 300) &
        (df['1.1'] >= 301) & (df['1.1'] <= 1140)
    ]

    if not filtered_df.empty:
        # Save the filtered data to a new Excel file
        output_file_path = 'filtered_excel_file_loop.xlsx'  # Replace with output file path
        filtered_df.to_excel(output_file_path, index=False)
        print("Filtered data saved to", output_file_path)

        # Load the Excel file into a DataFrame
        df = pd.read_excel(output_file_path)

        # Create a set to store unique rows
        unique_rows = set()

        # Create a list to store duplicate rows
        duplicate_rows = []

        # Iterate through each row in the DataFrame, starting from the second row
        for index, row in df.iloc[1:].iterrows():
            # Convert the row to a tuple to make it hashable
            row_tuple = tuple(row)

            # Check if the row is already in the set of unique rows
            if row_tuple in unique_rows:
                # If it's a duplicate, add it to the list of duplicate rows
                duplicate_rows.append(row)
            else:
                # If it's not a duplicate, add it to the set of unique rows
                unique_rows.add(row_tuple)

        # Create a new DataFrame containing the duplicate rows
        duplicate_df = pd.DataFrame(duplicate_rows, columns=df.columns)

        # Save the duplicate data to a new Excel file named 'loop.xlsx' without including the header
        duplicate_output_file_path = 'temp_loop.xlsx'
        duplicate_df.to_excel(duplicate_output_file_path, index=False, header=False)
        print("Duplicate data saved to", duplicate_output_file_path)

        # Get the second column of duplicate_df, get unique values, and write the length in the first cell of column 3
        unique_values = duplicate_df.iloc[:, 1].unique()
        length_of_unique_values = len(unique_values)

        # Load 'loop.xlsx'
        loop_df = pd.read_excel(duplicate_output_file_path, header=None)

        # Update the first cell of column 3 with the length of unique values
        loop_df.at[0, 2] = length_of_unique_values

        # Save the updated DataFrame to 'loop.xlsx'
        loop_df.to_excel(duplicate_output_file_path, index=False, header=False)
        print(f"Length of unique values in the second column written to the first cell of column 3 in {duplicate_output_file_path}")

        # Print the duplicate rows
        print("Duplicate Rows:")
        print(duplicate_df)

        # Print the number of duplicate rows
        print(f"Number of Duplicate Rows: {len(duplicate_df)}")

    else:
        print("No rows found that meet the criteria.")

except FileNotFoundError:
    print("The specified file was not found.")
except Exception as e:
    print("An error occurred:", e)


# Save the length of duplicate DataFrame in the Excel file
analysis_file_path = 'analysis.xlsx'
try:
    with pd.ExcelWriter(analysis_file_path) as writer:
        # Create a DataFrame with the number of duplicates and write it to the first cell of the first column
        df_len = pd.DataFrame([[len(duplicate_df)]], columns=None)
        df_len.to_excel(writer, sheet_name='loop', index=False, header=False, startrow=0, startcol=0)
    print(f"Number of duplicate rows saved in {analysis_file_path} under the sheet 'loop'")
except Exception as e:
    print(f"An error occurred while saving the number of duplicate rows: {e}")