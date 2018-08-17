import pymongo
from ConfigParser import SafeConfigParser
import argparse
from loremipsum import get_sentences
import os
from multiprocessing import Process
from os.path import expanduser
import random
from datetime import datetime
import sys
import threading
from pprint import pprint
import time
import names

# Globals
_DBNAME = "demodb"
_COLNAME = "democollection"
_THREADS = 10
_MAXBLOCKS = 1000
_BLOCKSIZE = 1000

def cli():
    try:
        global _DBNAME, _COLNAME, _THREADS, _MAXBLOCKS, _BLOCKSIZE

        parser = argparse.ArgumentParser(description='CLI Tool for continually writing random data to a MongoDB database for testing purposes')
        # config string
        parser.add_argument('-c', action="store", dest="cs", help="server connection string")
        parser.add_argument('-t', action="store", dest="t", help="threads to use, if left off, use 10")
        parser.add_argument('-b', action="store", dest="b", help="blocksize to use. if not inclided, use 1000")

        # functionality 
        parser.add_argument('task', metavar='task', help="clean, insert, insertAndUpdate, read, everything")

        # flags
        #parser.add_argument("-w", "--wait", help="wait until sandbox is completed until script returns", action="store_true")

        arg = parser.parse_args()
        homedir = expanduser("~")

        if (arg.cs != None):
            cp = SafeConfigParser()
            cp.add_section("mdb")
            cp.set('mdb', 'cs', arg.cs)

            with open(homedir+"/.mdbrandomizer", 'wb') as configfile:
                cp.write(configfile)

        elif (os.path.isfile(homedir+"/.mdbrandomizer")):
            cp = SafeConfigParser()
            cp.read(homedir+"/.mdbrandomizer")
        else:
            print "\nMust provide credentials or have a credential file\n"
            parser.print_help()
            exit(4)

        if(arg.t != None):
            _THREADS = int(arg.t)

        if(arg.b != None):
            _MAXBLOCKS = int(arg.b)

        if (arg.task.lower() == "clean"):
            clearDB(cp)
        elif (arg.task.lower() == "insert"):
            insertDB(cp)
        elif (arg.task.lower() == "insertandupdate"):
            updateDB(cp)
        elif (arg.task.lower() == "everything"):
            everythingDB(cp)
        elif (arg.task.lower() == "read"):
            readDB(cp)
        else:
            print "\nDidn't understand any task\n"
            parser.print_help()
            exit(5)

    except KeyboardInterrupt:
        print "\n\nCompleted!\n\n"
        exit(0)

def clearDB(cp):
    global _DBNAME, _COLNAME
    try:
        conn = pymongo.MongoClient(cp.get('mdb','cs'))
        conn.drop_database(_DBNAME)
        print "DB Dropped!"
    except:
        print "Could not clear the DB!"
        print sys.exc_info()[0]
        exit(6)

def insertDB(cp):
    global _DBNAME, _COLNAME, _THREADS, _MAXBLOCKS, _BLOCKSIZE
    conn = pymongo.MongoClient(cp.get('mdb','cs'))

    print "\n\n================================================="
    print "About to enter data in: "
    print "\tThreads: " + str(_THREADS)
    print "\tDB: " + _DBNAME
    print "\tCollection: " + _COLNAME
    print "\tBlocksize: " + str(_BLOCKSIZE)
    print "\tMax Blocks: " + str(_MAXBLOCKS)
    print "=================================================\n\n"
    print "This process will continue until you press control+c or break \n\n"

    for index in range(0, _THREADS):
        p = Process(target=r_insertRecord, args=(conn[_DBNAME][_COLNAME],_MAXBLOCKS, _BLOCKSIZE))
        p.start()
        p.join()

def everythingDB(cp):
    global _DBNAME, _COLNAME, _THREADS

    # start inserting
    t = threading.Thread(target=insertDB, args=(cp,))
    t.start()

    time.sleep(5)

    readDB(cp)

def readDB(cp):
    global _DBNAME, _COLNAME, _THREADS
    conn = pymongo.MongoClient(cp.get('mdb','cs'))

    print "\n\n================================================="
    print "About to read data in: "
    print "\tThreads: " + str(_THREADS)
    print "\tDB: " + _DBNAME
    print "\tCollection: " + _COLNAME
    print "=================================================\n\n"
    print "This process will continue until you press control+c or break \n\n"

    for index in range(0, _THREADS):
        p = Process(target=r_readRecords, args=(conn[_DBNAME][_COLNAME],))
        p.start()
        p.join()
    
def r_readRecords(handle):
    for iteration in xrange(10):
        docs = handle.find()
        for doc in docs:
            temp = doc['accountNumber']
    r_readRecords(handle)

# RECURSIVE FUNCTION!
def r_insertRecord(handle, mb, bs):

    states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    
    for i in xrange(mb):
        docs = []
        for j in xrange(bs):
            docs.append(
                {
                    "accountNumber": random.randint(1,1000),
                    "fullname": names.get_full_name(),
                    "address": str(random.randint(1,999))+ " " + names.get_first_name() + " Rd.",
                    "state": states[random.randint(0,49)],
                    "zipcode": str(random.randint(10000,99999)),
                    "singupDate": datetime.utcnow(),
                    "payment": random.randrange(50,200,5),
                    "copay": random.randrange(20,60,10),
                    "deductible": random.randrange(100,500,100),
                    "notes": "".join(get_sentences(50)),
                    "prescriptions":get_sentences(random.randint(1,25))
                    }
                )
        handle.insert_many(docs)
    r_insertRecord(handle)