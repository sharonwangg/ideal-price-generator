import os
import csv

zip_to_avg_income = {}
with open(os.path.join('..', 'dataset', 'simple_mi_incomes.csv'), 'r') as avg_income_file:
    rows = csv.reader(avg_income_file)
    header = next(rows)

    for row in rows:
        zip = row[0]
        avg_income = row[1]
        zip_to_avg_income[zip] = avg_income

with open(os.path.join('..', 'dataset', 'internal+estated+dist.csv'), 'r') as infile:
    with open(os.path.join('..', 'dataset', 'internal+estated+dist+incomes.csv'), 'w') as outfile:
        in_rows = csv.reader(infile)
        in_variables = next(in_rows)

        csv_writer = csv.writer(outfile)
        csv_writer.writerow(in_variables + ['avg_income'])

        for in_row in in_rows:
            print(row_i)
            zip = in_row[4]
            if zip in zip_to_avg_income:
                avg_income = zip_to_avg_income[zip]
            else:
                avg_income = 'NA'

            csv_writer.writerow(in_row + [avg_income])
