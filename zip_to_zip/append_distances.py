import pgeocode # https://pypi.org/project/pgeocode/
from haversine import haversine, Unit # https://pypi.org/project/haversine/
import os
import csv

KM_TO_MI = 0.621371
RANDAZZO_COORDS = (42.674160, -82.96394)
RANDAZZO_ZIP = '48042'
DIST = pgeocode.GeoDistance('us')

with open(os.path.join('..', 'dataset', 'internal+estated.csv'), 'r') as infile:
    with open(os.path.join('..', 'dataset', 'internal+estated+dist.csv'), 'w') as outfile:
        in_rows = csv.reader(infile)
        in_variables = next(in_rows)

        csv_writer = csv.writer(outfile)
        csv_writer.writerow(in_variables + ['mi_from_randazzo'])

        for in_row in in_rows:
            home_lat = in_row[34]
            home_lon = in_row[35]

            if home_lat == 'NA' or home_lon == 'NA' or home_lat == '' or home_lon == '':
                home_zip = in_row[4]
                if home_zip == 'NA' or home_zip == '':
                    mi = 'NA'
                else:
                    km = DIST.query_postal_code(home_zip, RANDAZZO_ZIP)
                    mi = km * KM_TO_MI
            else:
                home_coords = (float(home_lat), float(home_lon))
                mi = haversine(home_coords, RANDAZZO_COORDS, unit='mi')

            csv_writer.writerow(in_row + [mi])
