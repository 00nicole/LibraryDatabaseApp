import sqlite3
import datetime

conn = sqlite3.connect("library.db")
cursor = conn.cursor()
conn.commit()

def findItem():
    title = input("\nPlease enter the title of the item: ").strip()
    with conn:
        cursor.execute("SELECT * FROM Item WHERE title LIKE ?", ('%' + title + '%',))
        items = cursor.fetchall()
        
        if items:
            print("\nFound", len(items), "matching result(s):")
            for index, item in enumerate(items, start=1):
                print(str(index) + ". " + item[2] + ": " + item[1] + " by " + item[4] + " | Genre: " + item[8] + " | Status: " + item[6])

            while True:
                try:
                    selection = int(input("\nEnter the corresponding number to select an item: ").strip())
                    if 1 <= selection <= len(items):
                        item = items[selection - 1]
                        print("\n--- Item Details ---")
                        print("Title:", item[1])
                        print("Type:", item[2])
                        print("Publication Year:", item[3])
                        print("Author:", item[4])
                        print("Publisher:", item[5])
                        print("Status:", item[6])
                        print("Genre:", item[8])
                        
                        if item[6].lower() == "available":
                            while True:
                                borrows = input("\nWould you like to borrow this item? (yes/no): ").strip().lower()
                                if borrows == "yes":
                                    borrowItem(item[0])
                                    break
                                elif borrows == "no":
                                    print("Returning to main menu.")
                                    break
                                else:
                                    print("Invalid input. Please enter 'yes' or 'no'.")
                        break
                    else:
                        print("Invalid selection. Please enter a valid number.")
                except ValueError:
                    print("Invalid input. Please enter a numerical value.")
        else:
            print("\nSorry, no items found that match your search.")
   

def borrowItem(itemID):
    dueDate = (datetime.datetime.today() + datetime.timedelta(weeks=2)).strftime("%Y-%m-%d") 
    with conn:
        cursor.execute(
            "SELECT * FROM Borrowing WHERE libraryCardNumberFK = ? AND itemID_FK = ? AND returnDate IS NOT NULL",(libraryCardNumber, itemID))
        prevBorrowed = cursor.fetchone()

        cursor.execute(
            "UPDATE Item SET status = 'Borrowed' WHERE itemID = ?",(itemID,))
        if prevBorrowed:
             cursor.execute("UPDATE Borrowing SET dueDate = ?, returnDate = NULL, fine = 0 WHERE itemID_FK = ? AND libraryCardNumberFK = ?",(dueDate, itemID, libraryCardNumber))
        else:
            cursor.execute("INSERT INTO Borrowing (libraryCardNumberFK, itemID_FK, dueDate) VALUES (?, ?, ?)",(libraryCardNumber, itemID, dueDate))
    
    print(f"\nItem successfully borrowed! Please return the item by {dueDate}.")



def returnItem():
    with conn:
        cursor.execute(
            """SELECT b.itemID_FK, i.title, b.dueDate 
               FROM Borrowing b JOIN Item i ON b.itemID_FK = i.itemID 
               WHERE b.libraryCardNumberFK = ? AND b.returnDate IS NULL""",(libraryCardNumber,))
        borrowedItems = cursor.fetchall()
    if not borrowedItems:
        print("\nYou have no borrowed items to return.")
        return
    
    print("\nSelect an item to return:")
    for idx, (itemID, title, dueDate) in enumerate(borrowedItems, start=1):
        print(str(idx) + ". " + title + " (Due: " + dueDate + ")") 


    while True:
        try:
            selection = int(input("\nEnter the corresponding number of the item you want to return: "))
            if 1 <= selection <= len(borrowedItems):
                break
            else:
                print("Invalid selection. Please enter a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a numerical value.")

    itemID, title, dueDate = borrowedItems[selection - 1]
    returnDate = datetime.datetime.today()
    dueDate = datetime.datetime.strptime(dueDate, "%Y-%m-%d")
    fineAmt = max(0, (returnDate - dueDate).days)  

    with conn:
        cursor.execute("UPDATE Borrowing SET returnDate = ?, fine = ? WHERE itemID_FK = ? AND libraryCardNumberFK = ?",(returnDate.strftime("%Y-%m-%d"), fineAmt, itemID, libraryCardNumber))
        cursor.execute("UPDATE Item SET status = 'Available' WHERE itemID = ?",(itemID,))

    print(f"\n'{title}' has been successfully returned on {returnDate.strftime('%Y-%m-%d')}.")
    if fineAmt > 0:
        print(f"You have a fine of ${fineAmt} for the late return.")
    else:
        print("Thank you for returning on time!")


def donateItem():
    itemTitle = input("\nPlease enter the title of the item: ")
    itemType = input("\nPlease enter the item type (Book, DVD, Magazine, Newspaper, etc.): ")

    while True:
        try:
            publicationYear = int(input("\nPlease enter the publication year: "))
            if  publicationYear <= 2025:
                break
            else:
                print("\nSorry, the number must be a valid calendar year.\n")
        except ValueError:
            print("\nInvalid input. Please enter a numerical value.\n")
    
    authorName = input("\nPlease enter the name of the author: ")
    publisherName = input("\nPlease enter the name of the publisher: ")
    genre = input("\nPlease enter the genre of the item: ")

    with conn:
        #If the item already exists in the library, get the current quantity of this item, and increment it by 1
        cursor.execute(
            "SELECT quantity FROM Item WHERE title = ? AND type = ? AND publicationYear = ? AND authorName = ? AND publisherName = ? AND genre = ?",
            (itemTitle, itemType, publicationYear, authorName, publisherName, genre))
        
        currentQuantity = cursor.fetchone()

        if currentQuantity: 
            cursor.execute("UPDATE Item SET quantity = ? WHERE title = ? AND type = ? AND publicationYear = ? AND authorName = ? AND publisherName = ? AND genre = ?",
            (currentQuantity[0] + 1, itemTitle, itemType, publicationYear, authorName, publisherName, genre))
        
        else:
            cursor.execute("INSERT INTO Item (title, type, publicationYear, authorName, publisherName, status, quantity, genre) VALUES (?, ?, ?, ?, ?, 'Available', 1, ?)",
            (itemTitle, itemType, publicationYear, authorName, publisherName, genre))
        
    print("\nThank you for your donation of", itemTitle + " by", authorName + "!")


def findEvent():
    print("Select the event you are looking for:")
    print("1. Book Signing with George R.R. Martin\n2. AI and the Future of Work\n3. Space Exploration Talk\n4. National Geographic Documentary Screening\n5. Virtual Reality Gaming Expo")
    print("6. Climate Change and Its Impact\n7. Future of Renewable Energy Innovations\n8. Space Science for Kids\n9. Tech Talks: The Future of Artificial Intelligence\n10. The Rise of Electric Vehicles\n")
    
    with conn:
        cursor.execute("SELECT eventName, eventDate, recommendedAudience FROM Event WHERE eventID = ?",(getSelection(),))
    
        eventInfo = cursor.fetchone()
        print("Event Name:", eventInfo[0] + "\nEvent Date:", eventInfo[1] + "\nRecommended Audience:", eventInfo[2])


def registerForEvent():
    print("Select the event you would like to register for:")
    print("1. Book Signing with George R.R. Martin\n2. AI and the Future of Work\n3. Space Exploration Talk\n4. National Geographic Documentary Screening\n5. Virtual Reality Gaming Expo")
    print("6. Climate Change and Its Impact\n7. Future of Renewable Energy Innovations\n8. Space Science for Kids\n9. Tech Talks: The Future of Artificial Intelligence\n10. The Rise of Electric Vehicles\n")
   
    selection = getSelection()

    with conn:

        #Check if the user is already registered for the event
        cursor.execute("SELECT 1 FROM Attends WHERE libraryCardNumberFK = ? AND eventID_FK = ?",
        (libraryCardNumber, selection))

        alreadyRegistered = cursor.fetchone()

        #Get the event name
        cursor.execute("SELECT eventName FROM Event WHERE eventID = ?",
        ((selection,)))

        eventName = cursor.fetchone()

        if alreadyRegistered:
            print("You are already registered for the following event:", eventName[0])

        else:
            cursor.execute("INSERT INTO Attends (libraryCardNumberFK, eventID_FK) VALUES (?, ?)",
            (libraryCardNumber, selection))
            print("You have successfully registered for the following event:", eventName[0])
         

def volunteer():
    with conn:
        cursor.execute(
            """SELECT v.libraryNameFK, v.addressFK 
               FROM Volunteers v 
               WHERE v.libraryCardNumberFK = ?""",(libraryCardNumber,))
        volunteerAt = cursor.fetchall()

    if volunteerAt:
        print("\nYou are currently volunteering at the following library/libraries:")
        for index, (libraryName, address) in enumerate(volunteerAt, start=1):
            print(str(index) + ". " + libraryName + " ("+address+") ")
    else:
        print("\nYou are not currently volunteering at any libraries.")

    with conn:
        cursor.execute(
            """SELECT libraryName, address 
               FROM Library 
               WHERE (libraryName, address) NOT IN (
                   SELECT libraryNameFK, addressFK FROM Volunteers WHERE libraryCardNumberFK = ?
               )""",(libraryCardNumber,))
        availLibraries = cursor.fetchall()

    if not availLibraries:
        print("\nThere are no additional libraries available for volunteering.")
        return

    print("\nWould you like to volunteer at another library? Here are the available options:")
    for index, (libraryName, address) in enumerate(availLibraries, start=1):
        print(str(index) + ". " + libraryName + " ("+address+") ")

    while True:
        try:
            selection = input("\nPlease enter the corresponding number of the library that you would like to volunteer at (or 0 to cancel): ").strip()
            if selection == "0":
                print("\nReturning to menu...")
                return

            selection = int(selection)
            if 1 <= selection <= len(availLibraries):
                selected_library = availLibraries[selection - 1]
                break
            else:
                print("Invalid selection. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a numerical value.")
    with conn:
        cursor.execute(
            """INSERT INTO Volunteers (libraryNameFK, addressFK, libraryCardNumberFK) 
               VALUES (?, ?, ?)""",(selected_library[0], selected_library[1], libraryCardNumber))

    print("\nYou are now a volunteer at " + selected_library[0], "("+ selected_library[1]+"). Thank you for your support!")


def askForHelp():
    genre = input("State the genre you would like an item recommendation for (Action, Fantasy, Thriller, etc.): ").lower()

    with conn:
        
        cursor.execute("SELECT * FROM Item WHERE genre LIKE ?", ('%' + genre + '%',))

        itemRecommendation = cursor.fetchone()

        if itemRecommendation:
            print("The librarian recommends the ", itemRecommendation[2] + ":", itemRecommendation[1] + " by", itemRecommendation[4])
        else:
            print("Sorry, we currently have no items that match this genre.")

def getSelection():
    while True:
        try:
            selection = int(input("\nPlease enter a numerical value from 1 to 10: "))
            if 1 <= selection <= 10:
                return selection
            else:
                print("Sorry, the number must be between 1 and 10.\n")
        except ValueError:
            print("Invalid input. Please enter a numerical value.\n")




# into sequence
print("Welcome! Please select your library location:")
print("1. Central Library\n2. Eastside Branch\n3. West End Library\n4. South Park Library\n5. Uptown Library")
print("6. Downtown Library\n7. Northgate Branch\n8. Southside Library\n9. City Library\n10. Parkview Library\n")
libs = ["Central Library", "Eastside Branch", "West End Library", "South Park Library", "Uptown Library", "Downtown Library", "Northgate Branch", "Southside Library", "City Library", "Parkview Library"]

libLocation = libs[getSelection() - 1]

print("You have selected the",libLocation +".")

print("Please Enter Your Library Card Number:")
print("1. John Smith\n2. Emma Johnson\n3. Liam Williams\n4. Olivia Brown\n5. Noah Davis")
print("6. Ava Miller\n7. William Wilson\n8. Sophia Moore\n9. James Anderson\n10. Charlotte Taylor\n")
names = ["John Smith", "Emma Johnson", "Liam Williams", "Olivia Brown", "Noah Davis", "Ava Miller", "William Wilson", "Sophia Moore", "James Anderson", "Charlotte Taylor"]

libraryCardNumber = getSelection()
name = names[libraryCardNumber - 1]

print("\nWelcome to the Library,", name + "!")


def main():
    while True:
        print("\nTo make a selection, please enter the corresponding number")
        print("1. Find or borrow an item")
        print("2. Return an item")
        print("3. Donate an item")
        print("4. Find an event")
        print("5. Register for an event") 
        print("6. Volunteer")
        print("7. Ask for a recommendation")
        print("8. Exit")
        
        selection = input("Enter your selection: ")
        
        if selection == "1":
            findItem()
        elif selection == "2":
            returnItem()
        elif selection == "3":
            donateItem()
        elif selection == "4":
            findEvent()
        elif selection == "5":
            registerForEvent()
        elif selection == "6":
            volunteer()
        elif selection == "7":
            askForHelp()
        elif selection == "8":
            print("Exiting...")
            break
        else:
            print("Invalid selection. Please try again.")


if __name__ == "__main__":
    main()

conn.close()
