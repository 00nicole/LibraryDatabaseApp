import sqlite3

conn = sqlite3.connect("library.db")
cursor = conn.cursor()
conn.commit()

def findItem():
    print("implement me please")

def borrowItem():
    print("implement me please")

def returnItem():
    print("implement me please")

def donateItem():
    print("implement me please")

def findEvent():
    print("implement me please")

def registerForEvent():
    print("implement me please")

def volunteer():
    print("implement me please")

def askForHelp():
    print("implement me please")

# note: we might not even need to do this intro sequence
# we'll see once we do function implementation.
''' 
# intro sequence to get users to select location, then userID
print("Welcome! Please select your library location:")
print("1. Central Library\n2. Eastside Branch\n3. West End Library\n4. South Park Library\n5. Uptown Library")
print("6. Downtown Library\n7. Northgate Branch\n8. Southside Library\n9. City Library\n10. Parkview Library\n")
libs = ["Central Library", "Eastside Branch", "West End Library", "South Park Library", "Uptown Library", "Downtown Library", "Northgate Branch", "Southside Library", "City Library", "Parkview Library"]
while True:
    try:
        libLocation = int(input("Please enter a numerical value from 1 to 10: "))
        if 1 <= libLocation <= 10:
            print("You have selected",libs[libLocation-1] +".")
            break
        else:
            print("Sorry, the number must be between 1 and 10.\n")
    except ValueError:
        print("Invalid input. Please enter a numerical value.\n")

# Still need to add sign in for userID
while True:
    print("userID Signin :)")
    break

'''


def main():
    while True:
        print("\nWelcome to the Library!")
        print("\nTo make a selection, please enter the corresponding number")
        print("1. Find an item")
        print("2. Borrow an item") #should we merge with #1?
        print("3. Return an item")
        print("4. Donate an item")
        print("5. Find an event")
        print("6. Register for an event") #should we merge with number 5?
        print("7. Volunteer")
        print("8. Ask for help")
        print("9. Exit")
        
        selection = input("Enter your selection: ")
        
        if selection == "1":
            findItem()
        elif selection == "2":
            borrowItem()
        elif selection == "3":
            returnItem()
        elif selection == "4":
            donateItem()
        elif selection == "5":
            findEvent()
        elif selection == "6":
            registerForEvent()
        elif selection == "7":
            volunteer()
        elif selection == "8":
            askForHelp()
        elif selection == "9":
            print("Exiting...")
            break
        else:
            print("Invalid selection. Please try again.")


if __name__ == "__main__":
    main()

conn.close()
