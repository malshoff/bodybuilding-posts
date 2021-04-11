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

from bson.json_util import dumps
import re

app = Flask(__name__)


today = datetime.today()
yesterday = today - timedelta(days=1)
older = today - timedelta(days=2)  # threads 2 or more days old

dbconnection = os.environ.get("CONNECT_STRING")
connection = pymongo.MongoClient(dbconnection)
db = connection.misc
threads = db.threads


@app.route('/')
def hello_world(current=None, old=None, yesterdays=None, top=None, quantity=None):

    return render_template(
        "testing.html",

        top=threads.aggregate([
            {"$group": {"_id": '$op', "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 20},
        ]),

        quantity=threads.aggregate([
            {"$match":
                {"replies": {"$gte": 20}}
             },
            {"$group": {"_id": '$op', "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 20},
        ]),

        current=threads.find({
            'date': {'$gte': today},
            'replies': {'$gte': 20}
        }).sort('views', pymongo.DESCENDING),

        yesterdays=threads.find({
            "date": {'$gte': yesterday, '$lte': today},
            'replies': {'$gte': 80}}
        ).sort('views', pymongo.DESCENDING),

        old=threads.find({
            'date': {'$lte': older},
            '$or': [{'replies': {'$gte': 3000}}, {'views': {'$gte': 50000}}]
        })
    )


@app.route("/user/<string:name>")
def get_user(name):
    return dumps(threads.find({'op': re.compile(name, re.IGNORECASE)}))


@app.route("/users/")
def get_users():
    return dumps(threads.aggregate([
        {"$group": {"_id": '$op', "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]))


if __name__ == "__main__":

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
