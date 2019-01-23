# Bodybuilding Forum Archive

A Flask web application that displays the top posts of the day from the Bodybuilding.com's infamous "misc" forum.

## [View the demo site here](https://bb-archive.apps.pcfone.io/)

## Getting Started: Development Environment
Clone the repository 

```
git clone https://github.com/malshoff/bodybuilding-posts.git
```



### Prerequisites

The required Python 3 libraries are included in requirements.txt. Navigate to the parent directory and run

```
pip install -r requirements.txt
```

An environment variable will need to be set to tell flask which app to run (on windows replace "export" with "set"):

```
export FLASK_APP=hello.py
```

You will also need an environment variable containing the connection string (provided by [mlab](https://mlab.com)).

```
export CONNECT_STRING=$MLAB_CONNECT_STRING
```

Alternatively, edit hello.py so that CONNECT_STRING references a connection to your own MongoDB instance. The format of one document in the database is as follows:

```
{
    "_id": {
        "$oid": "5b9590dfa5b6b0f2aae6006a"
    },
    "title": "Sprite Zero is the best diet soda on the market",
    "url": "https://forum.bodybuilding.com/showthread.php?t=176190941&s=16dc44fe1941c6ccf94c476f27723c40",
    "replies": 32,
    "views": 591,
    "op": "Getter_done",
    "date": {
        "$date": "2018-09-10T03:24:30.959Z"
    }
}
```

## Running the Dev Server

Navigate to the root directory and run 

```
flask run
```

The app will run (by default) on localhost:5000

## Built With

* [Flask](http://flask.pocoo.org/) - The web framework used
* [PyMongo](https://api.mongodb.com/python/current/) - MongoDB API
* [mLab](https://mlab.com) - Free MongoDB hosting

