import os

def process_file(file_path, target_value):
    try:
        modified_values = []
        with open(file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                # Skip comment lines and lines that do not start with a number
                if line.strip() and not line.startswith(('#', '@')):
                    parts = line.split()
                    if len(parts) > 1:
                        try:
                            first_value = float(parts[0])
                            second_value = float(parts[1])
                            if first_value == target_value:
                                modified_values.append(second_value / 2)  # Divide the value in the second column by 2
                        except ValueError:
                            # Handle the case where conversion to float fails
                            continue
        return modified_values
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return []

def main():
    # Assuming the current directory contains the files
    folder_path = os.getcwd()  # Get the current working directory
    output_file = os.path.join(folder_path, 'results.txt')  # Save the output in the current directory

    file_paths = [f"msd-{i}.xvg" for i in range(1, 50)]  # File names without the full path
    target_value = 2000.000
    all_modified_values = []

    for file_path in file_paths:
        modified_values = process_file(file_path, target_value)
        all_modified_values.extend(modified_values)

    if all_modified_values:
        with open(output_file, 'w') as f:
            for value in all_modified_values:
                f.write(f"{value}\n")
        print(f"Modified values saved to {output_file}")
    else:
        print("No data with the specified value found.")

if __name__ == "__main__":
    main()
