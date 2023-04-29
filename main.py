import string

"""
    Student: Nicole-Rene Newcomb
    Class: CIS024C Python Programming
    Description: app manages concert seat availability
        and ticket sales with receipts for users.
"""

# Creates matrix (2D array) to represent seating chart
def create_seating(rows, columns):
    open_seat = '.'
    seating_matrix = [[open_seat for columns 
                       in range(0, columns)] for row 
                       in range(0, rows)]
    return seating_matrix

# Prints out entire seating chart with headers
def print_seating_chart(matrix, rows, columns):
    column_header = create_column_header(number_of_columns)
    seating_header = create_seating_header()
    print(seating_header)
    print(column_header)
    for row in range(number_of_rows):
        print("%02d" % (row), end="\t")
        [print(seating_matrix[row][column], end = " ") for column in range(number_of_columns)]
        print()

# Creates seating header to be displayed
def create_seating_header():
    seating_header = "\n\n" + "="*77 + "\n\tSEATING CHART\n" + "="*77 + "\n"
    return seating_header

# Creates column header to be displayed
def create_column_header(columns):
    column_header = ""
    alphabet_string = string.ascii_uppercase
    letter_line = "  \t"
    separator_line = "\t" + '-'*52 + "\t" + '-'*5 + "\t" + '-'*5

    for letter in alphabet_string:
        letter_line += str(letter) + " "
    
    letter_line += "\tType\tPrice"
    column_header = letter_line + "\n" + separator_line
    return column_header




number_of_rows = 20
number_of_columns = 26
seating_matrix = create_seating(number_of_rows, number_of_columns)
seating_matrix[8][6] = 'e'
seating_matrix[8][7] = 'e'
seating_matrix[8][8] = 'e'

print_seating_chart(seating_matrix, number_of_rows, number_of_columns)