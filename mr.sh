#!/bin/bash

echo "Running inserts and reads"
/usr/local/bin/MongoRandomizer -t 5 insert &
/usr/local/bin/MongoRandomizer -t 5 insert &
/usr/local/bin/MongoRandomizer -t 5 insert &
/usr/local/bin/MongoRandomizer read &
/usr/local/bin/MongoRandomizer read &

echo "Press any key to kill"
read w

killall MongoRanomizer
killall Python