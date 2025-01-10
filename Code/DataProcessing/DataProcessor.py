import csv

from pandas.core.interchange import column


class DataProcessor:
    def __init__(self):
        pass

    # Convert a string with multiple numbers separated by spaces into a list
    # of numbers and return the list
    def convert_to_numbers(self, numbers_string):
        # Split the string into a list of numbers
        numbers_list = numbers_string.split()

        # Convert the list elements to integers (or use float() for decimals)
        numbers = [int(num) for num in numbers_list]

        return numbers

    def create_row(self, rows, columns):
        row = {}
        for column, row_data in zip(columns, rows):
            row[column] = row_data
        return row

    def extract_str_rows_from_text(self, text_file_name, csv_file_name, column):
        # Open the file
        with open(text_file_name, 'r') as file:
            # Read all lines into a list
            lines = file.readlines()

        data = []
        for line in lines:
            data.append({column:line.strip()})

        with open(csv_file_name, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=[column])
            # Write the header
            writer.writeheader()
            # Write the data
            writer.writerows(data)

    def extract_int_rows_from_text(self, text_file_name, csv_file_name, columns):
        # Open the file
        with open(text_file_name, 'r') as file:
            # Read all lines into a list
            lines = file.readlines()

        data = []
        for line in lines:
            numbers = self.convert_to_numbers(line)
            row = self.create_row(numbers, columns)
            data.append(row)

        with open(csv_file_name, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=columns)
            # Write the header
            writer.writeheader()
            # Write the data
            writer.writerows(data)