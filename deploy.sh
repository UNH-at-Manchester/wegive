#!/bin/bash

# Given the following file directory:
# /wegive
# /wegive/wegive (production stuff)
# /wegive/deploy
# this script should be in /wegive/deploy.


# DO NOT DEFINE THIS IN THE REPO
SECRET_KEY=secret
mkdir /tmp/wegive.deploy
cd /tmp/wegive.deploy
git clone "https://github.com/UNH-at-Manchester/wegive.git"
cd wegive/wegive
rm -rf .git
rm db.sqlite3
if [ -e /usr/local/www/wegive/db.sqlite3 ] ; then
    cp /usr/local/www/wegive/db.sqlite3 .
else
    echo "no database!";
fi
sed "s/DEBUG = True/DEBUG = False/g" wegive/settings.py > wegive/settings.py.new
mv wegive/settings.py.new wegive/settings.py
sed "s/SECRET_KEY = .*/SECRET_KEY = '$SECRET_KEY'/g" wegive/settings.py > wegive/settings.py.new
mv wegive/settings.py.new wegive/settings.py
cd ..

if [ -e /usr/local/www/wegive ] ; then
    rm -rf /usr/local/www/wegive;
    mkdir /usr/local/www/wegive
fi

mv wegive /usr/local/www/

if [ -e db.sqlite3 ] ; then
    mv db.sqlite3 /usr/local/www/wegive/db.sqlite3
fi
cd
rm -rf /tmp/wegive.deploy
# should be done
