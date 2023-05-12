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
def menu_selections(user_selection, purchase_records, seating_matrix, rows, columns):
    
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
        
        menu_options(user_selection, purchase_records, seating_matrix, rows, columns)
        user_selection = '__'
    return

# Decision tree to direct calls based on user selection
def menu_options(user_selection, purchase_records, seating_matrix, rows, columns):
    if user_selection == 'v':
        print_seating(seating_matrix, rows, columns)
    elif user_selection == "b":
        buy_tickets(purchase_records, seating_matrix)
    elif user_selection == "d":
        display_all_purchases()
    elif user_selection == "s":
        search_for_purchase()
    
    return

# Buy ticket function requests user input to reserve seats
def buy_tickets(purchase_records, seating_matrix):
    letters_to_numbers_file = open(os.path.join(os.path.dirname(__file__), "column_letters_to_numbers.json"))
    numbers_to_letters_file = open(os.path.join(os.path.dirname(__file__), "column_numbers_to_letters.json"))
    letters_to_numbers = json.load(letters_to_numbers_file)
    numbers_to_letters = json.load(numbers_to_letters_file)
    is_int = False

    # Validates that user input is an integer value
    while not is_int:
        number_seats = input("\nPlease enter number of seats to buy: ")
        
        try:
            if number_seats.find('.') < 0 and int(number_seats):
                number_seats = int(number_seats)
                if number_seats > 0 and number_seats < 27:
                    is_int = True
                else:
                    print("\nPlease enter a number between 1-26. ")
            else:
                print("\nInvalid input: please enter a whole number over 0. ")
        except:
            print("\nInvalid input: please enter a numerical integer value.")
    
    # Select left-most seat from which seats will be assigned
    print("\nPick a seat using the 2 digit row number followed by a column letter.")
    print("For example, 02f, 09a, or 13m.")
    starting_seat = input("\nSelect the left-most seat to reserve: ")
    
    # Slice user entry to separate row from column and convert
    start_row = int(starting_seat[0:2]) - 1
    start_column = letters_to_numbers[str(starting_seat[2:3])]

    # Check if seats available
    for i in range(0, number_seats):
        if seating_matrix[start_row][start_column+i] != '.':
            print("\nSorry, your selection is not available.")
            return
    
    # Create list of seat numbers purchased
    seats_purchased = list()
    for i in range(0, number_seats):
        purchased_row = str(start_row)
        purchased_column = start_column + i
        column_letter = numbers_to_letters[str(purchased_column)]
        
        if len(purchased_row) == 1:
            purchased_row = '0' + purchased_row
        
        seat_number = purchased_row + column_letter
        seats_purchased.append(seat_number)


    # Call function to record transaction
    record_transaction(purchase_records, number_seats, seats_purchased, start_row, start_column)
    
    for i in range(0, number_seats):

        # Reserve user's selected seats
        seating_matrix[start_row][start_column + i] = 'X'

        # Add seats reserved for COVID spacing (e) in front and back
        if start_row == 0:
            seating_matrix[start_row + 1][start_column + i] = 'e'
        elif start_row == 19:
            seating_matrix[start_row - 1][start_column + i] = 'e'
        else:
            seating_matrix[start_row + 1][start_column + i] = 'e'
            seating_matrix[start_row - 1][start_column + i] = 'e'
    
    # Call function to add in COVID spacing seats around user's seats
    covid_spacing(seating_matrix, number_seats, start_row, start_column)

    letters_to_numbers_file.close()
    numbers_to_letters_file.close()

    return

# Adds COVID spacing seats around user's selected seats
def covid_spacing(seating_matrix, number_seats, start_row, start_column):

    # Add seats for COVID spacing (e) to left
    if start_column == 0:
        pass

    elif start_column == 1 and start_row not in [0, 19]:
        seating_matrix[start_row][start_column - 1] = 'e'
        seating_matrix[start_row + 1][start_column - 1] = 'e'
        seating_matrix[start_row - 1][start_column - 1] = 'e'
    
    elif start_column == 1 and start_row == 0:
        seating_matrix[start_row][start_column - 1] = 'e'
        seating_matrix[start_row + 1][start_column - 1] = 'e'
    
    elif start_column == 1 and start_row == 19:
        seating_matrix[start_row][start_column - 1] = 'e'
        seating_matrix[start_row - 1][start_column - 1] = 'e'    

    elif start_column > 1 and start_row not in [0, 19]:
        seating_matrix[start_row][start_column - 1] = 'e'
        seating_matrix[start_row][start_column - 2] = 'e'
        seating_matrix[start_row + 1][start_column - 1] = 'e'
        seating_matrix[start_row - 1][start_column - 1] = 'e'
        seating_matrix[start_row + 1][start_column - 2] = 'e'
        seating_matrix[start_row - 1][start_column - 2] = 'e'

    elif start_column > 1 and start_row == 0:
        seating_matrix[start_row][start_column - 1] = 'e'
        seating_matrix[start_row][start_column - 2] = 'e'
        seating_matrix[start_row + 1][start_column - 1] = 'e'
        seating_matrix[start_row + 1][start_column - 2] = 'e'

    elif start_column > 1 and start_row == 19:
        seating_matrix[start_row][start_column - 1] = 'e'
        seating_matrix[start_row][start_column - 2] = 'e'
        seating_matrix[start_row - 1][start_column - 1] = 'e'
        seating_matrix[start_row - 1][start_column - 2] = 'e'

    else:
        print("Sorry, you missed an edge case to the left.")


    # Add seats for COVID spacing (e) to right
    right_seat = start_column + number_seats - 1
    if right_seat == 25:
        pass

    elif right_seat == 24 and start_row not in [0, 19]:
        seating_matrix[start_row][right_seat + 1] = 'e'
        seating_matrix[start_row + 1][right_seat + 1] = 'e'
        seating_matrix[start_row - 1][right_seat + 1] = 'e'
    
    elif right_seat == 24 and start_row == 0:
        seating_matrix[start_row][right_seat + 1] = 'e'
        seating_matrix[start_row + 1][right_seat + 1] = 'e'

    elif right_seat == 24 and start_row == 19:
        seating_matrix[start_row][right_seat + 1] = 'e'
        seating_matrix[start_row - 1][right_seat + 1] = 'e'

    elif right_seat < 24 and start_row not in [0, 19]:
        seating_matrix[start_row][right_seat + 1] = 'e'
        seating_matrix[start_row][right_seat + 2] = 'e'
        seating_matrix[start_row + 1][right_seat + 1] = 'e'
        seating_matrix[start_row + 1][right_seat + 2] = 'e'
        seating_matrix[start_row - 1][right_seat + 1] = 'e'
        seating_matrix[start_row - 1][right_seat + 2] = 'e'

    elif right_seat < 24 and start_row == 0:
        seating_matrix[start_row][right_seat + 1] = 'e'
        seating_matrix[start_row][right_seat + 2] = 'e'
        seating_matrix[start_row + 1][right_seat + 1] = 'e'
        seating_matrix[start_row + 1][right_seat + 2] = 'e'

    elif right_seat < 24 and start_row == 19:
        seating_matrix[start_row][right_seat + 1] = 'e'
        seating_matrix[start_row][right_seat + 2] = 'e'
        seating_matrix[start_row - 1][right_seat + 1] = 'e'
        seating_matrix[start_row - 1][right_seat + 2] = 'e'

    else:
        print("Sorry, you missed an edge case to the right.")

    return

# Records purchase transaction details: name, email, etc.
def record_transaction(purchase_records, number_seats, seats_purchased, start_row, start_column):
    name = input("\nPlease enter your name: ")
    email = input("\nPlease enter your email: ")
    tickets = number_seats
    mask_cost = 5 * number_seats

    if start_row < 5:
        seat_type = "Front"
        ticket_cost = 80 * tickets
    
    elif start_row < 11:
        seat_type = "Middle"
        ticket_cost = 50 * tickets
    
    else:
        seat_type = "Back"
        ticket_cost = 25 * tickets

    sub_total = ticket_cost + mask_cost
    tax = round(sub_total * 0.0725, 2)
    total = sub_total + tax

    purchase_records[name] = [email, tickets, seat_type, seats_purchased, ticket_cost, mask_cost, sub_total, tax, total]

    print_receipt(purchase_records, name)
    return

# Prints out user's receipt for transaction
def print_receipt(purchase_records, name):
    receipt_header = "\n\n" + "="*77 + "\n\tRECEIPT\n" + "="*77 + "\n"
    print(receipt_header)
    print("-" * 77)
    print("Name\t\t: ", name)
    print("Email\t\t: ", purchase_records[name][0])
    print("No. of Tickets\t: ", purchase_records[name][1])
    print("Seat Type\t: ", purchase_records[name][2])
    print("Seat No.\t: ", purchase_records[name][3])
    print("Ticket Cost\t: ", purchase_records[name][4])
    print("Mask Fee\t: ", purchase_records[name][5])
    print("Sub-total\t: ", purchase_records[name][6])
    print("Tax\t\t: ", purchase_records[name][7])
    print("Name\t\t: ", name)
    print("Total\t\t: ", purchase_records[name][8])
    print("Name\t\t: ", name)
    

# Saves seating chart and purchase history to JSON files
def quit_program(seating_matrix, purchase_records):
    with open("seating.json", "w") as outfile1:
        json.dump(seating_matrix, outfile1)
    with open("purchases.json", "w") as outfile2:
        json.dump(purchase_records, outfile2)

    outfile1.close()
    outfile2.close()

    return

user_selection = '__'
rows = 20
columns = 26
seating_matrix = create_seating(rows, columns)
purchase_records = dict()

# Call function to display menu and accept user input
menu_selections(user_selection, purchase_records, seating_matrix, rows, columns)

# Call function to save JSON files before exiting app
quit_program(seating_matrix, purchase_records)