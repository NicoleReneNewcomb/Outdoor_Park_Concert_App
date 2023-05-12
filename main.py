import os.path
import string
import json

"""
    Student: Nicole-Rene Newcomb
    Class: CIS024C Python Programming
    Description: app manages concert seat availability
        and ticket sales with receipts for users.
"""

# Opens JSON file or creates matrix (2D array) as seating chart
def create_seating(rows, columns):
        
    #Opens JSON seating file, if exists
    try:
        open_seating_file = open(os.path.join(os.path.dirname(__file__), "seating.json"))
        seating_matrix = json.load(open_seating_file) 
    except IOError:
        print("Error: Sorry, file can't be opened " + open_seating_file)
        open_seat = '.'
        seating_matrix = [[open_seat for columns 
                            in range(0, columns)] for row 
                            in range(0, rows)]           
        raise IOError
    finally:
        return seating_matrix

# Prints the app menu for user selections
def print_menu():
    menu_header = create_menu_header()
    print(menu_header)
    print("\t[b] Buy")
    print("\t[v] View Seating")
    print("\t[s] Search for Customer Purchase Receipt by Name")
    print("\t[d] Display All Purchases and Total Sales Amount")
    print("\t[q] Quit")
    print("\n")

def create_menu_header():
    menu_header = "\n\n" + "="*77 + "\n\tOutdoor Park Concert App\n" + "="*77 + "\n"
    return menu_header

# Prints out entire seating chart with headers
def print_seating(matrix, rows, columns):

    column_header = create_column_header(columns)
    seating_header = create_seating_header()
    print(seating_header)
    print(column_header)
    for row in range(rows):

        # Since 0 is an uncommon row number in US, I added 1 to each row #
        print("%02d" % (row + 1), end="\t")
        [print(seating_matrix[row][column], end = " ") for column in range(columns)]
        if row < 5:
            print("\tFront\t $80")
        elif row < 11:
            print("\tMiddle\t $50")
        else:
            print("\tBack\t $25")
    print()
    return

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

# Menu function to display menu and accept user input
def menu_selections(user_selection, seating_matrix, rows, columns):
    
    # Loop to display menu and accept user input
    while len(user_selection) != 1:
        print_menu()

        user_selection = input("Please enter your selection: ").lower()

        if user_selection == 'q': 
            break

        while user_selection not in ['q', 'b', 'v', 's', 'd']:
            print("\nPlease enter a single letter (i.e. v)")
            user_selection = '__'
            break
        
        menu_options(user_selection, seating_matrix, rows, columns)
        user_selection = '__'
    return

# Decision tree to direct calls based on user selection
def menu_options(user_selection, seating_matrix, rows, columns):
    if user_selection == 'v':
        print_seating(seating_matrix, rows, columns)
    elif user_selection == "b":
        buy_ticket()
    elif user_selection == "d":
        display_all_purchases()
    elif user_selection == "s":
        search_for_purchase()


def quit_program(seating_matrix, purchase_records):
    with open("seating.json", "w") as outfile1:
        json.dump(seating_matrix, outfile1)
    with open("purchases.json", "w") as outfile2:
        json.dump(purchase_records, outfile2)

    outfile1.close()
    outfile2.close()

user_selection = '__'
rows = 20
columns = 26
seating_matrix = create_seating(rows, columns)
purchase_records = dict()

# Call function to display menu and accept user input
menu_selections(user_selection, seating_matrix, rows, columns)

# Call function to save JSON files before exiting app
quit_program(seating_matrix, purchase_records)