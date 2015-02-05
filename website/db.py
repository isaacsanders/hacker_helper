import psycopg2

conn = psycopg2.connect(database="hacker", user="dax", password="daxiscool")

def get_hacker(id):
    cur = conn.cursor()
    cur.callproc("get_hacker", (id,))
    user = cur.fetchone()
    if user is not None:
        name, fb_token = user
        cur.close()
        return {
            "name": name,
            "fb_oauth_access_token": fb_token
        }
    else:
        return None
