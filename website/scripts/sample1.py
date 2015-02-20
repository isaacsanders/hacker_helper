__author__ = 'daxx'

from db import *
import sys,json,requests,os
import urllib
f = open("output.txt","w")


hackathon_id = sys.argv[1]
hacker_id = sys.argv[2]

f.write("hackerId:"+ str(hacker_id))

r =  get_hackathon_data(str(hacker_id),str(hackathon_id))
dic = {}

for number, question, answer in r:
    dic[question] = answer
f.write("\n")
f.write(str(dic))
order = ['Email address', 'Favorite Color', 'Example projects', 'Linkedin', 'Check me out']

to_ret = []
for i in order:
    if i in dic:
        to_ret.append(dic[i])
    else:
        print "Don't have all the info"
        raise
    # to_ret.append(dic[i])

s = ",".join(to_ret)

f.write("curl 127.0.0.1:7003/log_to_file/"+urllib.quote(s))

os.popen("curl 127.0.0.1:7003/log_to_file/"+urllib.quote(s))


f.write("\nfinished")