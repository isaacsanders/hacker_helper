import csv
from daterangeparser import parse

import re
from unicodedata import normalize

from db import conn

import psycopg2

def process_hackathon_data(csvfile):
    cur = conn.cursor()

    reader = csv.reader(csvfile)
    reader.next() # header row
    for row in reader:
        logo_url, date_range, location, website, name, cover_image_url = row
        start_date, end_date = parse(date_range)
        start_date = psycopg2.Date(start_date.year, start_date.month, start_date.day)
        end_date = psycopg2.Date(end_date.year, end_date.month, end_date.day)

        slug = slugify(name, delim="_")
        path = "/hacker_helper/scripts/{0}".format(slug)

        cur.callproc("register_hackathon", (name,
                                            logo_url,
                                            cover_image_url,
                                            start_date,
                                            end_date,
                                            path))

    cur.close()
    conn.commit()

def slugify(text, delim=u'-'):
    _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.:]+')
    result = []
    for word in _punct_re.split(unicode(text).lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))
