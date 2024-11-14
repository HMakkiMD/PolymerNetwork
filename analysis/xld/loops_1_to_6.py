from collections import Counter

def save_numbers_with_occurrences(file_path, output_file, target_occurrence):
    with open(file_path, 'r') as file, open(output_file, 'w') as out_file:
        for line in file:
            numbers = list(map(int, line.strip().split()))
            first_number = numbers[0]
            occurrences = Counter(numbers[1:])
            for num, count in occurrences.items():
                if count == target_occurrence:
                    out_file.write(str(first_number) + " ")
                    break
        out_file.write("\n")

# Example usage:
input_file_path = "output.txt"  # Replace with the path to your input text file

# Save numbers with 6 occurrences
output_file_path = "loop_6.txt"  # Replace with the desired path for the output file
save_numbers_with_occurrences(input_file_path, output_file_path, 6)

# Save numbers with 5 occurrences
output_file_path = "loop_5.txt"
save_numbers_with_occurrences(input_file_path, output_file_path, 5)

# Save numbers with 4 occurrences
output_file_path = "loop_4.txt"
save_numbers_with_occurrences(input_file_path, output_file_path, 4)

# Save numbers with 3 occurrences
output_file_path = "loop_3.txt"
save_numbers_with_occurrences(input_file_path, output_file_path, 3)

# Save numbers with 2 occurrences
output_file_path = "loop_2.txt"
save_numbers_with_occurrences(input_file_path, output_file_path, 2)
###########################################
# Function to count numbers in the first line of a file and write the count in the second line
def count_numbers_in_first_line_and_write(file_name):
    try:
        with open(file_name, 'r+') as file:
            first_line = file.readline().strip()
            numbers = first_line.split()
            count = len(numbers)
            file.seek(0, 2)  # Move the cursor to the end of file
            file.write('\n' + str(count))  # Write count in the second line
    except FileNotFoundError:
        print(f"File '{file_name}' not found")

# List of file names
file_names = ['loop_6.txt', 'loop_5.txt', 'loop_4.txt', 'loop_3.txt', 'loop_2.txt']

# Iterate through each file and write the count of numbers in the second line
for file_name in file_names:
    count_numbers_in_first_line_and_write(file_name)

