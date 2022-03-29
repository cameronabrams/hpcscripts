#!/bin/bash

touch older.test
sleep 1
touch a.test
sleep 1
touch newer.test

#testfile='older.test'
#testfile="NONE"
testfile="newer.test"

if [ $testfile == "NONE" -o a.test -nt $testfile ]; then
    echo "Go"
else
    echo "Stop"
fi

