import psycopg2

conn = psycopg2.connect(database="hacker", user="dax", password="daxiscool")

def get_hacker(id):
    cur = conn.cursor()
    cur.callproc("get_hacker", id)
    user = cur.fetchone()
    print
    return user