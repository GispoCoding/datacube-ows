#!/bin/sh

wait-for-db
datacube-ows-update --schema --role opendatacube
python /code/update_ranges.py
datacube-ows-update --views
datacube-ows-update
flask run --host=0.0.0.0 --port=8000
