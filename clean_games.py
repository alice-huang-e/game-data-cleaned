import csv
import ast
from datetime import datetime

input_file = '/Users/alicehuang/Downloads/games.csv'
output_file = '/Users/alicehuang/Downloads/games_cleaned.csv'

def clean_list_field(field_str):
    """Convert list string to semicolon-separated format"""
    try:
        # Try to parse as Python literal (list)
        field_list = ast.literal_eval(field_str)
        if isinstance(field_list, list):
            return '; '.join(field_list)
        return field_str
    except:
        # If parsing fails, return as-is
        return field_str

def convert_k_notation(value_str):
    """Convert values like '3.9K' or '2M' to actual numbers"""
    try:
        value_str = value_str.strip()
        if value_str.endswith('K'):
            # Convert K to thousands
            num = float(value_str[:-1])
            return str(int(num * 1000))
        elif value_str.endswith('M'):
            # Convert M to millions
            num = float(value_str[:-1])
            return str(int(num * 1000000))
        else:
            return value_str
    except:
        return value_str

# Read and process the CSV
with open(input_file, 'r', encoding='utf-8') as infile, \
     open(output_file, 'w', encoding='utf-8', newline='') as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Process header
    header = next(reader)
    # Remove the first column (redundant index)
    if header and header[0] == '':
        header = header[1:]
    # Remove Summary column (index 7 after removing first column)
    if len(header) > 7:
        header = header[:7] + header[8:]
    writer.writerow(header)

    # Track seen rows to remove duplicates
    seen_rows = set()
    duplicates_removed = 0

    # Process each row
    for row in reader:
        # Remove the first column (redundant index)
        if row:
            row = row[1:]

        # Remove Summary column (index 7 after removing first column)
        if len(row) > 7:
            row = row[:7] + row[8:]

        # Clean Release Date (index 1: Title, Release Date, ...)
        if len(row) > 1 and row[1]:
            try:
                date_str = row[1].strip('"')
                date_obj = datetime.strptime(date_str, '%b %d, %Y')
                row[1] = str(date_obj.year)
            except Exception as e:
                # If parsing fails, keep the original value
                print(f"Could not parse date: {row[1]} - {e}")

        # Clean Team (index 2: Title, Release Date, Team, ...)
        if len(row) > 2 and row[2]:
            row[2] = clean_list_field(row[2])

        # Clean Genres (index 6: ..., Rating, Times Listed, Number of Reviews, Genres, ...)
        if len(row) > 6 and row[6]:
            row[6] = clean_list_field(row[6])

        # Convert K/M notation to numbers
        # Times Listed (index 4), Number of Reviews (index 5)
        # Plays (index 8), Playing (index 9), Backlogs (index 10), Wishlist (index 11)
        # (indices shifted after removing Summary column)
        numeric_indices = [4, 5, 8, 9, 10, 11]
        for idx in numeric_indices:
            if len(row) > idx and row[idx]:
                row[idx] = convert_k_notation(row[idx])

        # Check for duplicates before writing
        row_tuple = tuple(row)
        if row_tuple not in seen_rows:
            seen_rows.add(row_tuple)
            writer.writerow(row)
        else:
            duplicates_removed += 1

print(f"Cleaned CSV saved to: {output_file}")
print("Redundant index column has been removed.")
print("Summary column has been removed.")
print(f"Exact duplicate rows removed: {duplicates_removed}")
print("Release dates have been updated to show only the year.")
print("Team and Genres have been converted to semicolon-separated format.")
print("Numeric values with K/M notation have been converted to actual numbers.")
