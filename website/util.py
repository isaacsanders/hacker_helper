import csv
from daterangeparser import parse

import re
from unicodedata import normalize

from db import conn

def process_hackathon_data():
    with open("../Data/hackathons.csv") as csvfile:
        cur = conn.cursor()

        reader = csv.reader(csvfile)
        reader.next() # header row
        for row in reader:
            logo_url, date_range, location, website, name, cover_image_url = row
            start_date, end_date = parse(date_range)

            slug = slugify(name, delim="_")
            path = "/hacker_helper/scripts/{0}".format(slug)

            cur.callproc("register_hackathon", (name,
                                                logo_url,
                                                cover_image_url,
                                                location,
                                                start_date,
                                                end_date,
                                                path))


        cur.close()

def slugify(text, delim=u'-'):
    _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.:]+')
    result = []
    for word in _punct_re.split(unicode(text).lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))