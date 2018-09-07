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
        


#db = connection.misc
#threads = db.threads
        
app = Flask(__name__)
today = datetime.today()
yesterday = today - timedelta(days=1)
older = today - timedelta(days=2) #threads 2 or more days old
dbconnection = os.environ.get("CONNECT_STRING")

#currentThreads = threads.find({"date":{'$lte':today, '$gt':older}}).sort('views',pymongo.DESCENDING)


@app.route('/')
def hello_world(current= None,old = None,date=None,yesterday=None):
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
    return render_template(
        "hello.html",
        date = eastern,
        current=threads.find().sort('views',pymongo.DESCENDING), 
        yesterday = threads.find().sort('views',pymongo.DESCENDING),
        old = threads.find({"date":{'$lte':older}}).sort('views',pymongo.DESCENDING))
    
if __name__ == "__main__":
    
    port = int(os.environ.get('PORT', 5000))
    app.run(debug = True, host='0.0.0.0', port=port)