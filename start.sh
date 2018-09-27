#!/bin/bash

pipenv --python 3.7 install

# run the dev server
if [[ -n $DEBUG && $DEBUG == true ]]; then
    pipenv run flask run -h 0.0.0.0
else
    pipenv run gunicorn --config=config/gunicorn.py inhibition_bargraph:app
fi
