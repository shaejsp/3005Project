import psycopg2


class DatabaseConnection:
    def __init__(self):
        """
        sets up the connection to the DatabaseConnection
        """
        self.conn = psycopg2.connect(host="localhost", database="project",
                                    user="postgres", password="lucky")
        self.curs = self.conn.cursor()

    def logIn(self, user, p):
        """
        Check if a user's credentials are good or not.

        :param user: the username
        :param p: the user's password
        :return: True if the user's credentials are valid, False otherwise
        """
        self.curs.execute("select count(*) from customer where username = '{u}' and password = '{p}';".format(u=user, p=p))
        result = self.curs.fetchone()
        if result:
            if result[0] == 1:
                return True
        return False

    def usernameTaken(self, username):
        """
        Check if a username already exists in the database.

        :param username: the username
        :return: True if the username is already used, False, otherwise
        """
        self.curs.execute("select count(*) from customer where username = '{u}';".format(u=username))
        result = self.curs.fetchone()
        if result:
            if result[0] == 1:
                return True
        return False

    def register(self, user, p):
        """
        Puts a user's credentials in the database.

        :param user: the username
        :param p: the user's password
        """
        try:
            self.curs.execute("insert into customer (username, password) values ('{u}', '{p}');".format(u=user, p=p))
            self.conn.commit()
        except Exception as e:
            print(e)

    def getAuthorOf(self, ISBN):
        """
        Get the author of a book.

        :param ISBN: the ISBN of the book.
        :return: a list of tuples consisting of author names
        """
        try:
            self.curs.execute("select auth_name from author "
                              "where auth_id in (select auth_id from writes where isbn = '{i}');".format(i=ISBN))
            return self.curs.fetchall()
        except Exception as e:
            print(e)

    def searchByTitle(self, title):
        """
        Search for books by similar titles.

        :param title: the title we're searching for
        :return a list of tuples of books
        """
        title = "%" + title.replace(" ", "%") + "%"
        try:
            self.curs.execute("select * from book where title like '{t}';".format(t=title))
            result = self.curs.fetchall()
            return result
        except Exception as e:
            print(e)

    def searchByAuthor(self, author):
        """
        Search for books by similar authors.

        :param author: the author we're searching for
        :return a list of tuples of books
        """
        author = "%" + author.replace(" ", "%") + "%"
        try:
            self.curs.execute("select * from book where isbn in "
                              "(select isbn from writes where auth_id in "
                              "(select auth_id from author "
                              "where auth_name LIKE '{a}'));".format(a=author))
            return self.curs.fetchall()
        except Exception as e:
            print(e)

    def searchByGenre(self, genre):
        """
        Search for books by similar genres.

        :param genre: the genre we're searching for
        :return a list of tuples of books
        """
        genre = "%" + genre.replace(" ", "%") + "%"
        try:
            self.curs.execute("select * from book where isbn in "
                              "(select isbn from book_genre where genre_id in "
                              "(select g_id from genre "
                              "where g_name LIKE '{a}'));".format(a=genre))
            return self.curs.fetchall()
        except Exception as e:
            print(e)

    def searchByISBN(self, isbn):
        """
        Search for books by ISBN.

        :param isbn: the isbn we're searching for
        :return a list of tuples of books (should be 1 book or 0)
        """
        try:
            self.curs.execute("select * from book where isbn = '{i}';".format(i=isbn))
            return self.curs.fetchall()
        except Exception as e:
            print(e)

    def addToCart(self, isbn, quantity, user):
        """
        Adds a book to a user's cart.

        :param isbn: the book being added
        :param quantity: the number of books the user wants to buy
        :param user: the username
        """
        try:
            self.curs.execute("insert into book_in_cart (ISBN, quantity, cart_id) "
                              "values ('{i}', {q}, ("
            	              "select cart_id from customer "
            	              "where username = '{u}'));".format(i=isbn, q=quantity, u=user))
            self.conn.commit()
            return True
        except psycopg2.errors.UniqueViolation:  # already in db
            self.conn.commit()
            self.curs.execute("update book_in_cart "
                              "set quantity = quantity + {q} "
                              "where cart_id = "
                              "(select cart_id from customer "
                              "where username = '{u}') "
                              "and isbn = '{i}';".format(i=isbn, q=quantity, u=user))
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False



    def clearCart(self, user):
        """
        Remove everything from a user's cart.

        :param user: the username
        """
        try:
            self.curs.execute("delete from book_in_cart "
                              "where cart_id in (select cart_id from customer where username = '{u}');".format(u=user))
            self.conn.commit()
        except Exception as e:
            print(e)

    def addPostalArea(self, postal, province, country):
        """
        Adds a postal area to the database.

        :param postal: the postal or zip code
        :param: province: the province or state
        :param country: the country
        """
        try:
            postal = postal.replace(" ", "")
            self.curs.execute("insert into postal_area (postal_code, province, country)"
                              "values('{z}', '{p}', '{c}');".format(z=postal, p=province, c=country))
            self.conn.commit()
            return True
        except psycopg2.errors.UniqueViolation:  # already in db
            return True
        except Exception as e:
            print(e)


    def addAddress(self, street_num, street_name, city, postal):
        """
        Add an address to the database.

        :param street_num: the street number
        :param street_name: the name of the street
        :param city: the city
        :param postal: the postal or zip code
        """
        try:
            postal = postal.replace(" ", "")
            self.curs.execute("insert into address (street_num, street_name, city, postal_code)"
                              "values('{snu}', '{sna}', '{c}', '{p}');".format(snu=street_num, sna=street_name, c=city, p=postal))
            self.conn.commit()
            return True
        except psycopg2.errors.UniqueViolation:  # already in db
            return True
        except Exception as e:
            print(e)

    def getAddressId(self, street_num, street_name, city, postal):
        """
        Get the address id of an address.

        :param street_num: the street number
        :param street_name: the name of the street
        :param city: the city
        :param postal: the postal or zip code
        :return a list of tuples of address ids (should be 1 or 0)
        """
        try:
            postal = postal.replace(" ", "")
            self.curs.execute("select addr_id from address "
                              "where street_num = '{snu}' "
                              "and street_name = '{sna}' "
                              "and city = '{c}' "
                              "and postal_code = '{p}';".format(snu=street_num,
                                                             sna=street_name,
                                                             c=city,
                                                             p=postal))
            return self.curs.fetchall()
        except Exception as e:
            print(e)

    def addBilling(self, username, addr_id):
        """
        Add a billing address to a user.

        :param username: the username
        :param addr_id: the address id
        """
        try:
            self.curs.execute("insert into customer_billing (cust_id, addr_id) "
                "values ("
            	"(select cust_id from customer "
            	"where username = '{u}'), {a});".format(u=username, a=addr_id))
            self.conn.commit()
            return True
        except psycopg2.errors.UniqueViolation:  # already in db
            self.curs.execute("update customer_billing "
                              "set addr_id = {a} where cust_id = "
                              "(select cust_id from customer "
                              "where username = '{u}');".format(a=addr_id, u=username))
            self.conn.commit()
            return True
        except Exception as e:
            print(e)

    def addShipping(self, username, addr_id):
        """
        Add or update a shipping address to a user.

        :param username: the username
        :param addr_id: the address id
        """
        try:
            # see if in db
            self.curs.execute("select * from customer_shipping "
                              "where cust_id = "
                              "(select cust_id from customer "
                              "where username = '{u}');".format(u=username))
            if len(self.curs.fetchall()) > 0:  # user is in the db - we update
                self.curs.execute("update customer_shipping "
                                   "set addr_id = {a} where cust_id = "
                                   "(select cust_id from customer "
                                   "where username = '{u}');".format(a=addr_id, u=username))
            else:
                self.curs.execute("insert into customer_shipping (cust_id, addr_id) "
                    "values ("
                	"(select cust_id from customer "
                	"where username = '{u}'), {a});".format(u=username, a=addr_id))
            self.conn.commit()
            return True
        except Exception as e:
            print(e)

    def addBillingAsShipping(self, username):
        """
        Add a user's billing address as their shipping address.

        :param username: the username
        """
        try:
            self.curs.execute("insert into customer_shipping (cust_id, addr_id)"
                              "values((select cust_id from customer "
                              "where username = '{u}'), "
                              "(select addr_id from customer_billing "
                              "where cust_id = "
                              "(select cust_id from customer "
                              "where username = '{u}')));".format(u=username))
            self.conn.commit()
        except Exception as e:
            print(e)

    def getBooksInCart(self, username):
        """
        Get the books in a user's cart.

        :param username: the username
        :return: a list of tuples of isbns, cart_ids, and quantities
        """
        try:
            self.curs.execute("select * from book_in_cart "
                              "where cart_id = (select cart_id from customer "
                              "where username = '{u}');".format(u=username))
            return self.curs.fetchall()
        except Exception as e:
            print(e)


    def deleteBookFromCart(self, username, isbn):
        """
        Remove a book from a user's cart (regardless of quantity).

        :param username: the username
        :param isbn: the isbn of the book
        """
        try:
            self.curs.execute("delete from book_in_cart "
                              "where cart_id = (select cart_id from customer "
                              "where username = '{u}') and isbn = '{i}';".format(u=username, i=isbn))
            self.conn.commit()
        except Exception as e:
            print(e)

    def updateCartQuantity(self, username, isbn, quantity):
        """
        Update the quantity of a book in a user's cart.

        :param username: the username
        :param isbn: the isbn of the book
        :param quantity: the new quantity
        """
        try:
            self.curs.execute("update book_in_cart "
                              "set quantity = {q} "
                              "where cart_id = "
                              "(select cart_id from customer "
                              "where username = '{u}') "
                              "and isbn = '9780439358071';".format(q=quantity, u=username, i=isbn))
            self.conn.commit()
        except Exception as e:
            print(e)

    def getBillingAddr(self, username):
        """
        Get the billing address for a user.

        :param username: the username
        :return: a list of tuples of address information
        """
        try:
            self.curs.execute("select addr_id from customer_billing "
	                          "where cust_id = "
	 	                      "(select cust_id from customer "
		                      "where username = '{u}');".format(u=username))
            return self.curs.fetchall()
        except Exception as e:
            print(e)

    def getShippingAddr(self, username):
        """
        Get the shipping address for a user.

        :param username: the username
        :return: a list of tuples of address information
        """
        try:
            self.curs.execute("select addr_id from customer_shipping "
	                          "where cust_id = "
	 	                      "(select cust_id from customer "
		                      "where username = '{u}');".format(u=username))
            return self.curs.fetchall()
        except Exception as e:
            print(e)

    def getAddress(self, addr_id):
        """
        Get address information.

        :param addr_id: the id of the address
        :return: a list of tuples of address information
        """
        try:
            self.curs.execute("select * from address "
	                          "where addr_id = {a};".format(a=addr_id))
            return self.curs.fetchall()
        except Exception as e:
            print(e)

    def getProvCountry(self, postal):
        """
        Get the province and country from a postal code.

        :param postal: the postal code
        :return: a list of tuples of postal area information
        """
        try:
            self.curs.execute("select * from postal_area "
	                          "where postal_code = '{p}';".format(p=postal))
            return self.curs.fetchall()
        except Exception as e:
            print(e)

    def purchaseCart(self, username, shippingAddr, isbns):
        """
        Create a purchase and transfer all of the books in book_in-cart to
        book_purchased.

        :param username: the username
        :param shippingAddr: the id of the shipping address
        :param isbns: a list of isbns of books in the cart
        """
        try:
            self.curs.execute("insert into purchase (cust_id, addr_id) "
                              "values((select cust_id from customer "
                              "where username = '{u}'),"
                              "{a})".format(u=username, a=shippingAddr))
            self.conn.commit()
            # add all of the books in books_in_cart to book_purchased

            for isbn in isbns:
                self.curs.execute("insert into book_purchased (ISBN, quantity, order_id) "
                                  "values ('{i}', "
    		                      "(select quantity from book_in_cart "
    		 	                  "where book_in_cart.cart_id = "
    		 	                  "(select cust_id from customer where username = '{u}') "
    		 	                  "and isbn = '{i}'), "
    		                      "(select order_id from purchase "
    		 	                  "where cust_id = (select cust_id from customer where username = '{u}')));".format(i=isbn, u=username))
                self.conn.commit()
            self.clearCart(username)
        except Exception as e:
            print(e)
