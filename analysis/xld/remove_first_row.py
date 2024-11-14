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
file_path = "connection_molecule.xlsx"

# Call the function to delete the first row
delete_first_row_excel(file_path)
