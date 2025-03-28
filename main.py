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
        cursor.execute("SELECT eventName, eventDate, recommendedAudience FROM Event WHERE eventID = ?",
        (getSelection(),))
    
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
    print("implement me please")

def askForHelp():
    genre = input("State the genre you would like an item recommendation for (Action, Fantasy, Thriller, etc.): ")

    with conn:
        
        cursor.execute("SELECT * FROM Item WHERE genre = ? LIMIT 1",
        (genre,))

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

# note: we might not even need to do this intro sequence
# we'll see once we do function implementation.

# intro sequence to get users to select location, then userID
print("Welcome! Please select your library location:")
print("1. Central Library\n2. Eastside Branch\n3. West End Library\n4. South Park Library\n5. Uptown Library")
print("6. Downtown Library\n7. Northgate Branch\n8. Southside Library\n9. City Library\n10. Parkview Library\n")
libs = ["Central Library", "Eastside Branch", "West End Library", "South Park Library", "Uptown Library", "Downtown Library", "Northgate Branch", "Southside Library", "City Library", "Parkview Library"]


libLocation = libs[getSelection() - 1]

print("You have selected the",libLocation +".")


#Sign in using library card number
print("Please Enter Your Library Card Number:")
print("1. John Smith\n2. Emma Johnson\n3. Liam Williams\n4. Olivia Brown\n5. Noah Davis")
print("6. Ava Miller\n7. William Wilson\n8. Sophia Moore\n9. James Anderson\n10. Charlotte Taylor\n")
names = ["John Smith", "Emma Johnson", "Liam Williams", "Olivia Brown", "Noah Davis", "Ava Miller", "William Wilson", "Sophia Moore", "James Anderson", "Charlotte Taylor"]

libraryCardNumber = getSelection()
name = names[libraryCardNumber - 1]

print("\nWelcome to the Library", name + "!")


def main():
    while True:
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
