import psycopg2

conn = psycopg2.connect(database="hacker", user="dax", password="daxiscool")

def get_hacker(id):
    with conn.cursor() as cur:
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

def get_friends(user_id):
    with conn.cursor() as cur:
        cur.callproc("get_friends", (user_id,))
        friends = []
        for (fid, email, name, lid) in cur.fetchall():
            friends.append(
            { "id": fid
            , "email": email
            , "name": name
            , "location_id": lid
            })
        return friends

def get_hackathons_attended(user_id):
    with conn.cursor() as cur:
        cur.callproc("get_hackathons_attending_from_hacker_id", (user_id,))
        hackathons = []
        for (hid, name) in cur.fetchall():
            hackathons.append(
            { "id": hid
            , "name": name
            })
        return hackathons

def get_hackathon(hackathon_id):
    with conn.cursor() as cur:
        cur.callproc("get_hackathon", (hackathon_id,))
        hackathon = cur.fetchone()
        if hackathon is not None:
            id, name, logo_url, cover_image_url, location_id, start_date, end_date, state, city, zipcode, country, street_number, route, website = hackathon
            cur.close()
            directions_url = "http://maps.google.com?daddr=" + '+'.join([street_number, route,
                                                                                    city, state,
                                                                                    zipcode, country]).replace(" ", "+")
            return { "id": id
                    , "name": name
                    , "logo_url": logo_url
                    , "cover_image_url": cover_image_url
                    , "start_date": start_date
                    , "end_date": end_date
                    , "directions_url": directions_url
                    , "website": website
                    }
        else:
            return None