import psycopg2

conn = psycopg2.connect(database="hacker", user="dax", password="daxiscool")

def get_hacker(id):
    with conn.cursor() as cur:
        cur.callproc("get_hacker", (id,))
        user = cur.fetchone()
        if user is not None:
            name, fb_token = user
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

def get_friends_at_hackathon(user_id,hackathon_id):
    friends = get_friends(user_id)
    friends_going = []
    for friend in friends:
        hackathons = get_hackathons_attended(friend["id"])
        for hackathon in hackathons:
            if hackathon["id"]==hackathon_id:
                friends_going.append(str(friend["name"]))
    return friends_going

def is_going(facebook_id,hackathon_id):
    id = get_hacker_from_oauth(facebook_id)["id"]
    hackathons = get_hackathons_attended(id)
    print hackathons
    for hackathon in hackathons:
        if int(hackathon_id)==int(hackathon["id"]):
            return True
    return False

def add_friend(facebook_id, friend_id):
    id = str(get_hacker_from_oauth(facebook_id)["id"])
    with conn.cursor() as cur:
        cur.callproc("add_friend", (int(id),int(friend_id)))
        conn.commit()
        return str(cur.fetchall())

def is_friends(facebook_id,friend_id):
    id = get_hacker_from_oauth(facebook_id)["id"]
    print id,friend_id
    print str(id)==str(friend_id)
    if str(id)==str(friend_id):
        return "You"
    friends = get_friends(int(friend_id))
    for friend in friends:
        if friend["id"]==id:
            return "Friend"
    return "Not Friend"





def get_hackathons():
    with conn.cursor() as cur:
        cur.callproc("get_hackathons", ())
        hackathons = []
        for hackathon in cur.fetchall():
            id, name, logo_url, cover_image_url, start_date, end_date, script, state, city, zipcode, country, street_number, route = hackathon

            hackathons.append(
            { "id": id
            , "name": name
            , "logo_url": logo_url
            , "cover_image_url": cover_image_url
            , "start_date": start_date
            , "end_date": end_date
            , "location": ",".join([street_number, route, city, state, zipcode, country])
            })
        return hackathons

def register_for_hackathon(hackathon_id, user_id):
    with conn.cursor() as cur:
        user_id = get_hacker_from_oauth(user_id)["id"]
        cur.callproc("register_user_for_hackathon", (hackathon_id, user_id))
        conn.commit()
        return cur.fetchall()



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
            id, name, logo_url, cover_image_url, start_date, end_date, state, city, zipcode, country, street_number, route, website = hackathon
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

def add_team(creator_id, team_name):
    with conn.cursor() as cur:
        cur.callproc("add_team", (creator_id, team_name))
        team_id = cur.fetchone()
        conn.commit()
        return team_id

def get_hacker_from_oauth(oauth_token):
    with conn.cursor() as cur:
        cur.callproc("get_hacker_from_oauth", (oauth_token,))
        id, email, location_id, name = cur.fetchone()
        return { "id": id
               , "email": email
               , "location_id": location_id
               , "name": name
               }

def add_hacker_to_team(member_id, team_id):
    with conn.cursor() as cur:
        cur.callproc("add_hacker_to_team", (member_id, team_id))