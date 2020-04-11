import json
import random
import psycopg2

"""
bookdata.json from:
https://gitlab.com/jagger27/bookdata/-/blob/master/bookdata.json
"""

def getBookData(book):
    data = {}
    data['isbn'] = book['isbn13']
    data['title'] = book['title']
    data['num_pages'] = book['page_count']
    data['price'] = random.randint(10, 20) + 0.99
    data['quantity'] = 0
    data['pub_percent'] = float("{:.2f}".format(random.uniform(0.05, 0.20)))
    data['year'] = book['year']
    data['summary'] = book['description']
    return data

def insertBook(book, curs):
    query = 'INSERT into book'
    query += " values ('{title}', {isbn}, {num_pages}, {price}, {quantity}, {pub_percent}, {year}, '{summary}');".format(**book)
    curs.execute(query)


def insertAuthor(authors, curs):
    for author in authors:
        try:
            query = "insert into author (auth_name) values('{a}');".format(a=author)
            curs.execute(query)
        except psycopg2.errors.UniqueViolation:
            print("Author is already in the database")


def getAuthId(author, curs):
        check = "select * from author where auth_name = '{a}';".format(a=author)
        curs.execute(check)
        result = curs.fetchone()
        if result:
            return result[0]
        else:
            return -1


def main():
    with open('bookdata.json', encoding="utf8") as f:
        books = json.load(f)

    conn = psycopg2.connect(host="localhost",database="project", user="postgres", password="lucky")
    curs = conn.cursor()

    for b in books:
        data = getBookData(b)
        insertBook(data, curs)
        conn.commit()
        insertAuthor(b['authors'], curs)
        conn.commit()
        print("A ID: ", getAuthId('Suzanne Colins', curs))

        break

    # curs.execute('SELECT * FROM book')
    # db_version = curs.fetchone()
    # print(db_version)
    #
    # curs.execute('SELECT * FROM author')
    # db_version = curs.fetchone()
    # print(db_version)

    # curs.execute('DELETE FROM book;')
    # curs.execute('DELETE FROM author;')
    conn.commit()

    curs.close()
    conn.close()


if __name__ == '__main__':
    main()
