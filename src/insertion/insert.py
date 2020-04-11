import json
import random
import psycopg2

"""
bookdata.json from:
https://gitlab.com/jagger27/bookdata/-/blob/master/bookdata.json
"""

def getBookData(book):
    """
    Get relevant data from a JSON book object for db insertion. Generates
    random numbers for the price ($10.99-$20.99) and publicer percent (5%-20%)

    :param book: the book as a dictionary (JSON)
    :return: a dictionary containing the isbn, title, number of pages, price,
        quantity, publisher percent, year published, and summary
    """
    data = {}
    data['isbn'] = book['isbn13']
    data['title'] = book['title']
    data['title'] = data['title'].replace("'", "''")
    data['num_pages'] = book['page_count']
    data['price'] = random.randint(10, 20) + 0.99
    data['quantity'] = 0
    data['pub_percent'] = float("{:.2f}".format(random.uniform(0.05, 0.20)))
    data['year'] = book['year']
    data['summary'] = book['description']
    data['summary'] = data['summary'].replace("'", "''")
    return data


def insertBook(book, curs):
    """
    Insert a book into the database.

    :param book: a dictionary of values for the book
    :param curs: the cursor for the connection to the database
    :return: True if the book was inserted successfully, False otherwise
    """
    query = 'INSERT into book '
    query += "values ('{title}', {isbn}, {num_pages}, {price}, {quantity}, {pub_percent}, {year}, '{summary}');".format(**book)
    try:
        curs.execute(query)
        return True
    except Exception as e:
        print("Error inserting {b} into book".format(b=book['title']))
        print("-- {}".format(e))
        return False


def insertAuthor(author, curs):
    """
    Insert a book into the database.

    :param author: the name of the author being inserted into the database
    :param curs: the cursor for the connection to the database
    """
    try:
        query = "insert into author (auth_name) values('{a}');".format(a=author)
        curs.execute(query)
    except psycopg2.errors.UniqueViolation:
        print("Author {a} is already in the database".format(a=author))
    except Exception as e:
        print("Error inserting {a} into author".format(a=author))
        print("-- {}".format(e))


def getAuthId(author, curs):
    """
    Get the id of an author from the database.

    :param author: the name of the author
    :param curs: the cursor for the connection to the database
    :return: the id of the author if found, otherwise -1
    """
    check = "select * from author where auth_name = '{a}';".format(a=author)
    curs.execute(check)
    result = curs.fetchone()
    if result:
        return result[0]
    else:
        return -1


def insertWrites(a_id, isbn, curs):
    """
    Insert an author and book into the writes relation.

    :param a_id: the id of the author of the book
    :param isbn: the isbn of the book the author wrote
    :param curs: the cursor for the connection to the database
    """
    try:
        query = "insert into writes values({i}, '{a}');".format(i=isbn, a=a_id)
        curs.execute(query)
    except psycopg2.errors.UniqueViolation:
        print("{a} and {i} already in writes relation".format(a=a_id, i=isbn))
    except Exception as e:
        print("Error inserting {a} and {i} into writes".format(a=aid, i=isbn))
        print("-- {}".format(e))


def insertGenre(genre, curs):
    """
    Insert a genre into the genre relation.

    :param genre: the name of the genre
    :param curs: the cursor for the connection to the database
    """
    try:
        query = "insert into genre (g_name) values('{g}');".format(g=genre)
        curs.execute(query)
    except psycopg2.errors.UniqueViolation:
        print("{g} already in genre relation".format(g=genre))
    except Exception as e:
        print("Error inserting {g} into genre".format(g=genre))
        print("-- {}".format(e))


def insertBookGenre(g_id, isbn, curs):
    """
    Insert a book and corresponding genre into the database.

    :param g_id: the id of the genre
    :param isbn: the isbn of the book
    :param curs: the cursor for the connection to the database
    """
    try:
        query = "insert into book_genre values({g}, '{i}');".format(i=isbn, g=g_id)
        curs.execute(query)
    except psycopg2.errors.UniqueViolation:
        print("{g} and {i} already in book_genre relation".format(g=g_id, i=isbn))
    except Exception as e:
        print("Error inserting {g} and {i} into book_genre".format(g=g_id, i=isbn))
        print("-- {}".format(e))


def getGenreId(genre, curs):
    """
    Get the id of a genre from the database.

    :param genre: the name of the genre
    :param curs: the cursor for the connection to the database
    :return: the id of the genre if found, else -1
    """
    check = "select * from genre where g_name = '{g}';".format(g=genre)
    curs.execute(check)
    result = curs.fetchone()
    if result:
        return result[0]
    else:
        return -1


def insertPublisher(publisher, curs):
    """
    Insert a publisher into the publisher relation. Sets the email to the
    publisher's name without spaces @gmail.com and creates a random phone
    number and bank account number.

    :param publisher: the name of the publisher
    :param curs: the cursor for the connection to the database
    """
    try:
        email = publisher.replace(" ", "") + "@gmail.com"
        phone = ''.join(["{}".format(random.randint(0, 9)) for num in range(0, 10)])
        bank_acct = ''.join(["{}".format(random.randint(0, 9)) for num in range(0, 12)])

        query = "insert into publisher (pub_name, email, phone, bank_acct) "
        query += "values('{pn}', '{e}', {p}, {b});".format(pn=publisher, e=email, p=phone, b=bank_acct)
        curs.execute(query)
    except psycopg2.errors.UniqueViolation:
        print("{p} already in publisher relation".format(p=publisher))
    except Exception as e:
        print("Error inserting {p} into publisher".format(p=publisher, e=e))
        print("-- {}".format(e))


def getPublisherId(publisher, curs):
    """
    Get the id of a publisher in the database.

    :param publisher: the name of the publisher
    :param curs: the cursor for the connection to the database
    :return: the id of the publisher if found, otherwise -1
    """
    check = "select * from publisher where pub_name = '{p}';".format(p=publisher)
    curs.execute(check)
    result = curs.fetchone()
    if result:
        return result[0]
    else:
        return -1


def insertPublished(p_id, isbn, curs):
    """
    Insert a book and the respective publisher into the database.

    :param p_id: the id of the publisher
    :param isbn: the isbn of the book
    :param curs: the cursor for the connection to the database
    """
    try:
        query = "insert into published values({p}, '{i}');".format(i=isbn, p=p_id)
        curs.execute(query)
    except psycopg2.errors.UniqueViolation:
        print("{p} and {i} already in published relation".format(p=p_id, i=isbn))
    except Exception as e:
        print("Error inserting {p} and {i} into book_genre".format(p=p_id, i=isbn))
        print("-- {}".format(e))


def main():
    with open('bookdata.json', encoding="utf8") as f:
        books = json.load(f)

    conn = psycopg2.connect(host="localhost", database="project",
                            user="postgres", password="lucky")
    curs = conn.cursor()

    for b in books:  # loops through all of the books
        data = getBookData(b)
        success = insertBook(data, curs)
        conn.commit()

        if not success:
            continue

        for a in b['authors']:  # loops through all authors for this book
            a = a.replace("'", "''")
            insertAuthor(a, curs)
            conn.commit()

            a_id = getAuthId(a, curs)
            if a_id != -1:
                insertWrites(a_id, data['isbn'], curs)
                conn.commit()

        if b['tags']:
            for g in b['tags']:  # loops through all of the tags for this book
                insertGenre(g, curs)
                conn.commit()

                g_id = getGenreId(g, curs)
                if g_id != -1:
                    insertBookGenre(g_id, data['isbn'], curs)
                    conn.commit()

        for p in b['publishers']:
            p = p.replace("'", "''")
            insertPublisher(p, curs)
            conn.commit()

            p_id = getPublisherId(p, curs)
            if p_id != -1:
                insertPublished(p_id, data['isbn'], curs)
                conn.commit()

    curs.close()
    conn.close()


if __name__ == '__main__':
    main()
