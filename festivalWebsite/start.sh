#!/bin/bash
pip install -e .
export FLASK_APP=festivalWebsite
export FLASK_ENV=development
export FLASK_DEBUG=1
[[ ! $# -eq 0 ]] && flask init-db
flask run
