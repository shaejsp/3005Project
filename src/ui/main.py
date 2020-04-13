from queries import *

global db
db = DatabaseConnection()

class StartMenu:
    """
    The start menu of the application, allows the user to log in, sign up,
    or exit.
    """
    def __init__(self):
        self.display()
        self.navigate()

    def display(self):
        """ Display the menu and get the user's choice. """
        choice = input("\nPlease enter your choice:"
                       "\n\t1. Log in "
                       "\n\t2. Sign Up "
                       "\n\t3. Quit\n")
        try:
            self.choice = int(choice)
        except:
            StartMenu()

    def navigate(self):
        """ Navigate to the next page based on the user's choice. """
        if self.choice == 1:
            LogIn()
        elif self.choice == 2:
            SignUp()
        elif self.choice == 3:
            exit(0)
        else:
            print("\nPlease enter a valid choice.\n")
            StartMenu()


class LogIn:
    def __init__(self):
        self.display()
        self.navigate()

    def display(self):
        """ Display the menu and get the user's choice. """
        print("\n--- Log in ---")
        print("To go back, enter b as username.")
        user = input("Username: ")
        if user == 'b':
            StartMenu()
        password = input("Password: ")

        self.success = db.logIn(user, password)
        global username
        username = user

    def navigate(self):
        """ Navigate to the next page based on the user's choice. """
        if self.success == True:
            HomeMenu()
        else:
            print("\nYour username or password was incorrect.")
            LogIn()


class SignUp:
    def __init__(self):
        self.display()
        self.addToDatabase()
        self.navigate()

    def display(self):
        """ Display the menu and get the user's choice. """
        print("--- Sign Up ---")
        user = input("Username: ")

        if db.usernameTaken(user):
            print("\nSorry, that username has already been taken.\n")
            SignUp()
        else:
            global username
            username = user
            self.password = input("Password: ")

    def addToDatabase(self):
        """ Add a new user to the database. """
        db.register(username, self.password)

    def navigate(self):
        """ Navigate to the next pages. """
        EnterBillingAddr()
        EnterShippingAddr()
        HomeMenu()


class EnterBillingAddr():
    def __init__(self):
        self.display()
        self.addToDatabase()

    def display(self):
        """ Display the menu and get the user's choice. """
        print("\n--- Billing Address ---")
        self.streetNum = input("Street number: ")
        self.streetName = input("Street name: ")
        self.city = input("City: ")
        self.province = input("Province/State: ")
        self.postalCode = input("Postal code/zip code: ")
        self.country = input("Country: ")

    def addToDatabase(self):
        """ Add a new billing address to the database and associate it with the user. """
        if db.addPostalArea(self.postalCode, self.province, self.country):
            db.addAddress(self.streetNum, self.streetName, self.city, self.postalCode)
            addr_id = db.getAddressId(self.streetNum, self.streetName, self.city, self.country)
            db.addBilling(username, addr_id[0][0])


class EnterShippingAddr():
    def __init__(self):
        self.display()
        self.addToDatabase()

    def display(self):
        """ Display the menu and get the user's choice. """
        print("\n--- Shipping Address ---")
        self.same = input("Is your shipping address the same as your billing address? (y/n) ")
        if self.same == "y" or self.same == "Y":
            return
        self.streetNum = input("Street number: ")
        self.streetName = input("Street name: ")
        self.city = input("City: ")
        self.province = input("Province/State: ")
        self.postalCode = input("Postal code/zip code: ")
        self.country = input("Country: ")

    def addToDatabase(self):
        """ Add a shipping address to the database and associate it with the user. """
        if self.same == 'y' or self.same == "Y":
            db.addBillingAsShipping(username)
        else:
            if db.addPostalArea(self.postalCode, self.province, self.country):
                db.addAddress(self.streetNum, self.streetName, self.city, self.postalCode)
                addr_id = db.getAddressId(self.streetNum, self.streetName, self.city, self.country)
                db.addBilling(username, addr_id[0][0])


class HomeMenu:
    def __init__(self):
        self.display()
        self.navigate()

    def display(self):
        """ Display the menu and get the user's choice. """
        choice = input("\nPlease enter your choice:"
                       "\n\t1. Search by title"
                       "\n\t2. Search by genre"
                       "\n\t3. Search by author"
                       "\n\t4. Search by ISBN"
                       "\n\t5. View cart"
                       "\n\t6. Check out"
                       "\n\t7. Log out"
                       "\n\t8. Quit\n")
        try:
            self.choice = int(choice)
        except:
            HomeMenu()

    def navigate(self):
        """ Navigate to the next page based on the user's choice. """
        if self.choice == 1:
            SearchByTitle()
        elif self.choice == 2:
            SearchByGenre()
        elif self.choice == 3:
            SearchByAuthor()
        elif self.choice == 4:
            SearchByISBN()
        elif self.choice == 5:
            CartView()
        elif self.choice == 6:
            CheckOut()
        elif self.choice == 7:
            StartMenu()
        elif self.choice == 8:
            exit(0)
        else:
            HomeMenu()

class SearchByTitle:
    def __init__(self):
        self.display()
        self.getBooks()
        self.navigate()

    def display(self):
        """ Display the search and get the title. """
        print("--- Search By Title ---")
        self.title = input("Enter title: ")

    def getBooks(self):
        """ Get a list of books with similar titles. """
        self.books = db.searchByTitle(self.title)

    def navigate(self):
        """ Navigate to the next page based on the user's choice. """
        if len(self.books) == 0:
            print("Sorry, there are no books with names similar to " + self.title)
            HomeMenu()
        else:
            PostSearchMenu(self.books)


class SearchByGenre:
    def __init__(self):
        self.display()
        self.getBooks()
        self.navigate()

    def display(self):
        """ Display the search and get the genre. """
        print("--- Search By Genre ---")
        self.genre = input("Enter genre: ")

    def getBooks(self):
        """ Get a list of books with similar genre. """
        self.books = db.searchByGenre(self.genre)

    def navigate(self):
        """ Navigate to the next page based on the user's choice. """
        if len(self.books) == 0:
            print("Sorry, there are no books with genres similar to " + self.genre)
            HomeMenu()
        else:
            PostSearchMenu(self.books)


class SearchByAuthor:
    def __init__(self):
        self.display()
        self.getBooks()
        self.navigate()

    def display(self):
        """ Display the search and get the author. """
        print("--- Search By Author ---")
        self.author = input("Enter author: ")

    def getBooks(self):
        """ Get a list of books with a similar author. """
        self.books = db.searchByAuthor(self.author)

    def navigate(self):
        """ Navigate to the next page based on the user's choice. """
        if len(self.books) == 0:
            print("Sorry, there are no books with authors similar to " + self.author)
            HomeMenu()
        else:
            PostSearchMenu(self.books)


class SearchByISBN:
    def __init__(self):
        self.display()
        self.getBooks()
        self.navigate()

    def display(self):
        """ Display the search and get the ISBN. """
        print("--- Search By ISBN ---")
        self.isbn = input("Enter ISBN: ")

    def getBooks(self):
        """ Get a list of books with that ISBN. """
        self.books = db.searchByISBN(self.isbn)

    def navigate(self):
        """ Navigate to the next page based on the user's choice. """
        if len(self.books) == 0:
            print("Sorry, there are no books with ISBN = " + self.isbn)
            HomeMenu()
        else:
            PostSearchMenu(self.books)


class PostSearchMenu:
    def __init__(self, books):
        self.books = books
        self.printBooks()
        self.display()
        self.navigate()

    def printBooks(self):
        """ Print the books resulting from a search. """
        for i in range(len(self.books)):
            book = self.books[i]
            authors = db.getAuthorOf(book[1])
            authStr = ""
            for a in authors:
                authStr += a[0] + ", "
            authStr = authStr[:-2]

            print("{:2}. {:55s} {:50s} {:<10f} ${}".format(i+1, book[0], authStr, book[6], book[3]))

    def display(self):
        """ Display the menu and get the user's choice. """
        choice = input("\nPlease enter your choice:"
                       "\n\t1. Add a book to your cart"
                       "\n\t2. Back"
                       "\n\t3. View cart"
                       "\n\t4. Check out"
                       "\n\t5. Log out"
                       "\n\t6. Quit\n")
        try:
            self.choice = int(choice)
        except:
            PostSearchMenu(self.books)

    def navigate(self):
        """ Navigate to the next page based on the user's choice. """
        if self.choice == 1:
            AddToCart(self.books)
        elif self.choice == 2:
            HomeMenu()
        elif self.choice == 3:
            CartView()
        elif self.choice == 4:
            CheckOut()
        elif self.choice == 5:
            StartMenu()
        elif self.choice == 6:
            exit(0)


class AddToCart:
    def __init__(self, books):
        self.books = books
        self.display()
        self.addToCart()
        self.navigate()

    def display(self):
        """ Display the menu and get the user's choice. """
        bookNum = input("What is the number of the book you'd like to buy: ")
        self.bookIndex = int(bookNum) - 1
        if self.bookIndex >= len(self.books):
            print("That is not a valid book number.")
            AddToCart(self.books)
        quantity = input("How many would you like to buy: ")
        self.quantity = int(quantity)

    def addToCart(self):
        """ Add a book to the user's cart. """
        db.addToCart(self.books[self.bookIndex][1], self.quantity, username)

    def navigate(self):
        """ Navigate to the next page based on the user's choice. """
        print()
        PostSearchMenu(self.books)


class CartView:
    def __init__(self):
        self.displayCart()
        self.displayMenu()
        self.navigate()

    def displayCart(self):
        """ Print the books in a user's cart. """
        self.books = db.getBooksInCart(username)

        print("\n--- Your Cart ---")
        print("    {:55s} {:50s} {:<7} {}".format("Title", "Author(s)", "Price", "Quantity"))

        for i in range(len(self.books)):
            isbn = self.books[i][0]
            quantity = self.books[i][2]
            authors = db.getAuthorOf(isbn)
            authStr = ""
            for a in authors:
                authStr += a[0] + ", "
            authStr = authStr[:-2]

            book = db.searchByISBN(isbn)[0]
            print("{:2}. {:55s} {:50s} ${:<6} {}".format(i+1, book[0], authStr, book[3], quantity))
        print()

    def displayMenu(self):
        """ Display the menu and get the user's choice. """
        choice = input("Please enter your choice: "
                       "\n\t1. Remove a book from your cart"
                       "\n\t2. Change the quantity of a book"
                       "\n\t3. Empty your cart"
                       "\n\t4. Check out"
                       "\n\t5. Back to home"
                       "\n\t6. Log out"
                       "\n\t7. Quit\n")
        try:
            self.choice = int(choice)
        except:
            CartView()


    def navigate(self):
        """ Navigate to the next page based on the user's choice. """
        if self.choice == 1:
            self.removeBook()
        elif self.choice == 2:
            self.changeQuantity()
        elif self.choice == 3:
            db.clearCart(username)
            HomeMenu()
        elif self.choice == 4:
            CheckOut()
        elif self.choice == 5:
            HomeMenu()
        elif self.choice == 6:
            LogIn()
        elif self.choice == 7:
            exit(0)
        else:
            print("\nPlease enter a valid choice.")
            CartView()

    def removeBook(self):
        """ Remove a book from a user's cart. """
        bookIndex = input("What is the number of the book you'd like to remove from your cart? ")
        bookIndex = int(bookIndex) - 1
        db.deleteBookFromCart(username, self.books[bookIndex][0])

    def changeQuantity(self):
        """ Change the quantity of a book in the user's cart. """
        bookIndex = input("What is the number of the book you'd like to remove from your cart? ")
        bookIndex = int(bookIndex) - 1
        quantity = int(input("How many would you like to buy? "))
        db.updateCartQuantity(username, self.books[bookIndex][0], quantity)


def main():
    StartMenu()  # starts the program


if __name__ == '__main__':
    main()
