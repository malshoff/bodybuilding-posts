import pymongo
import os

from datetime import datetime, timedelta
from dateutil import tz

import connexion
from flask import Flask
from flask import render_template

from bson.json_util import dumps
import re

dbconnection = os.environ.get("CONNECT_STRING")
connection = pymongo.MongoClient(dbconnection)
db = connection.misc
threads = db.threads

def users(name):
    return dumps(threads.find({'op':re.compile(name,re.IGNORECASE)}))