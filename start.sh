#!/bin/bash

if [ ! -d venv ]; then
    python3.7 -m venv venv
    source venv/bin/activate
    pip install -U pip
    pip install -r requirements.txt
    deactivate
fi

source venv/bin/activate

if [ ! -f requirements.txt ]; then
    pip install -r requirements-base.txt
    pip freeze > requirements.txt
fi

# run the dev server
if [[ -n $DEBUG && $DEBUG == true ]]; then
    flask run -h 0.0.0.0
else
    gunicorn --config=config/gunicorn.py inhibition_bargraph:app
fi
