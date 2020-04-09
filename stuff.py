import psycopg2

def main():
    conn = psycopg2.connect(host="localhost",database="project", user="postgres", password="lucky")
    curs = conn.cursor()
    curs.execute('SELECT * FROM book')
    db_version = curs.fetchone()
    print(db_version)
    curs.close()


if __name__ == '__main__':
    main()
