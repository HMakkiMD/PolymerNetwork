# this code give the melamine molecule numbers that form a loop
import pandas as pd
import re

def excel_to_text(excel_path, text_path):
    # Read the Excel file
    df = pd.read_excel(excel_path, header=None)  # Read without headers
    # Save the DataFrame to a text file, without ignoring any rows
    df.to_csv(text_path, sep='\t', index=False, header=False, float_format='%d')  # Save as integer

def check_repeated_numbers(text_path):
    with open(text_path, 'r') as file:
        lines = file.readlines()

    repeated_numbers = []  # List to store all repeated numbers
    
    for line in lines:
        numbers = line.strip().split()
        for number in numbers:
            if numbers.count(number) > 1:
                first_number = extract_first_number(line)
                if first_number is not None:
                    repeated_numbers.append(first_number)
                break  # Break out of inner loop after finding first repeated number
    
    return repeated_numbers

def extract_first_number(line):
    # Extract the first number from the line using regex
    match = re.search(r'\d+', line)
    if match:
        return match.group()
    return None

def main(excel_path, text_path):
    # Convert Excel to text file
    excel_to_text(excel_path, text_path)
    
    # Check for repeated numbers in each line
    repeated_numbers = check_repeated_numbers(text_path)
    
    # Save the repeated numbers horizontally in a single line with just a space between each number
    with open("primary_loops_molecule_number.txt", "w") as output_file:
        output_file.write(" ".join(repeated_numbers))

# Example usage:
# Replace 'mel_acr_junctions.xlsx' with the path to your Excel file
# Replace 'output.txt' with the path to the desired text file
excel_path = 'mel_acr_junctions.xlsx'
text_path = 'output.txt'

main(excel_path, text_path)
