# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 17:28:58 2016

@author: M
"""
import pymongo
import os


from datetime import datetime, timedelta
from dateutil import tz
from flask import Flask
from flask import render_template

"""
MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "misc"
MONGODB_COLLECTION = "threads"
"""
        
        
app = Flask(__name__)
today = datetime.today()
yesterday = today - timedelta(days=1)
older = today - timedelta(days=2) #threads 2 or more days old
dbconnection = os.environ.get("CONNECT_STRING")

connection = pymongo.MongoClient(dbconnection)
# Hardcode zones:
from_zone = tz.gettz('UTC')
to_zone = tz.gettz('US/Eastern')


utc = datetime.utcnow()


utc = utc.replace(tzinfo=from_zone)

# Convert time zone
eastern = utc.astimezone(to_zone)

db = connection.misc
threads = db.threads
print("Current:")
current=threads.find({
           "date":{'$gte':today}
        }).sort('views',pymongo.DESCENDING)

for x in current:
    print(x)
print("Yesterdays:")
yesterdays = threads.find({
            "date":{'$gte':yesterday, '$lte':today},
            'replies':{'$gte':80}
        }).sort('views', pymongo.DESCENDING)
for x in yesterdays:
    print(x)

#currentThreads = threads.find({"date":{'$lte':today, '$gt':older}}).sort('views',pymongo.DESCENDING)


