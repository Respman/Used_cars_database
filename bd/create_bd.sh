#! /usr/bin/env bash

./csv-parser.py
psql -f used_cars.sql
#если нужно сделать дамп базы данных:
#pg_dump -U postgres used_cars > ./used_cars.pgsql

rm condition.csv
rm drive.csv
rm fuel.csv
rm general_characteristics.csv
rm listing_location.csv
rm manufacturer.csv
rm model.csv
rm paint_color.csv
rm region.csv
rm size.csv
rm state.csv
rm title_status.csv
rm transmission.csv
rm type.csv
rm used_car.csv