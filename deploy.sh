#!/bin/bash

# Given the following file directory:
# /wegive
# /wegive/wegive (production stuff)
# /wegive/deploy
# this script should be in /wegive/deploy.


# DEFINE THIS
SECRET_KEY=secret
git clone "https://github.com/UNH-at-Manchester/wegive.git"
cd wegive/wegive
rm -rf .git
rm db.sqlite3
sed "s/DEBUG = True/DEBUG = False/g" wegive/settings.py > wegive/settings.py.new
mv wegive/settings.py.new wegive/settings.py
sed "s/SECRET_KEY = cd.*/SECRET_KEY = $SECRET_KEY/g" wegive/settings.py > wegive/settings.py.new
mv wegive/settings.py.new wegive/settings.py
cd ..

if [ -e ../../wegive ] ; then
    cd ../../wegive
    killall django
    cd ..
    mv wegive/wegive/db.sqlite3 .
    rm -rf wegive;
    mkdir wegive
    mkdir wegive/wegive
else
    cd ../../;
fi

mv deploy/wegive wegive

if [ -e db.sqlite3 ] ; then
    mv db.sqlite3 wegive/wegive/db.sqlite3
fi
# should be done
