import pandas as pd

# Load the Excel file
file_path = 'selected_rows.xlsx'
df = pd.read_excel(file_path)

# Remove rows where the values in the first and second columns are the same based on their position
df = df[df.iloc[:, 0] != df.iloc[:, 1]]

# Save the modified data to a new Excel file
new_file_path = 'deleted_rows.xlsx'
df.to_excel(new_file_path, index=False)

print("Rows with same values in the first and second columns based on position have been removed.")
from openpyxl import load_workbook

def delete_first_row_excel(file_path):
    try:
        # Load the workbook
        wb = load_workbook(file_path)
        
        # Select the active sheet
        sheet = wb.active
        
        # Delete the first row
        sheet.delete_rows(1)
        
        # Save the workbook
        wb.save(file_path)
        print("First row deleted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Provide the file path of your Excel file
file_path = "deleted_rows.xlsx"

# Call the function to delete the first row
delete_first_row_excel(file_path)