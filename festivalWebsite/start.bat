@echo off
set FLASK_APP=festivalWebsite
set FLASK_ENV=development
set FLASK_DEBUG=1
if [%1]==[] goto noDB
flask init-db
:noDB
flask run --host=0.0.0.0