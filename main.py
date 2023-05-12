import os.path
import string
import json

"""
    Student: Nicole-Rene Newcomb
    Class: CIS024C Python Programming
    Description: app manages concert seat availability
        and ticket sales with receipts for users.
"""

# Opens JSON or creates matrix (2D array) to represent seating chart
def create_seating(rows, columns):
        
    #Opens JSON seating file, if exists
    try:
        open_seating_file = open(os.path.join(os.path.dirname(__file__), "seating.json"))
        seating_matrix = json.load(open_seating_file) 
    except IOError:
        print("Error: Sorry, file can't be opened " + open_seating_file)
        raise IOError
    finally:
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



def quit_program(seating_matrix):
    json


open_seating_file = open_file()
number_of_rows = 20
number_of_columns = 26
seating_matrix = create_seating(number_of_rows, number_of_columns)


print_seating_chart(seating_matrix, number_of_rows, number_of_columns)