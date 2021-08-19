import csv
import os
import argparse

PARSER = argparse.ArgumentParser()
PARSER.add_argument('ZIPCODE')
PARSER.add_argument('JOB_TYPE')
ARGS = PARSER.parse_args()
CUSTOMER_ZIPCODE = ARGS.ZIPCODE
JOB_TYPE = ARGS.JOB_TYPE

print(JOB_TYPE)

# match zipcode to average income
MICHIGAN_INCOMES_FILEPATH = os.path.join('..', 'dataset', 'simple_mi_incomes.csv')
with open(MICHIGAN_INCOMES_FILEPATH, 'r') as michigan_incomes:
    rows = csv.reader(michigan_incomes)
    variables = next(rows)

    for row in rows:
        zipcode = row[0]
        avg_income = float(row[1])
        if zipcode == CUSTOMER_ZIPCODE:
            income_range = [avg_income - 10000, avg_income + 10000]

# if zipcode not in mi database, exit
if income_range is None:
    print('income data not available for zipcode '+CUSTOMER_ZIPCODE)
    exit()

# slice data based on job type and income
DATA_FILEPATH = os.path.join('..', 'dataset', 'median_price.csv')
data_slice = []
max_price = None
with open(DATA_FILEPATH, 'r') as randazzo_data:
    rows = csv.reader(randazzo_data)
    variables = next(rows)

    for row in rows:
        curr_job_type = row[6]
        try:
            avg_income = float(row[50])
        except:
            continue

        if curr_job_type == JOB_TYPE and avg_income >= income_range[0] and avg_income <= income_range[1]:
            data_slice.append(row)
            median_price = float(row[61])
            if max_price is None or median_price > max_price:
                max_price = median_price

print(data_slice)

# start "moving up the catplot"
miss_count = 0
increment = 100
median_price_start = 1000
price_range = [0.95 * median_price_start, 1.05 * median_price_start]

option_range_to_win_rate = {}

# while miss_count < 2 and price_range[0] <= max_price:
while price_range[0] <= max_price:
    price_slice = []
    sold_count = 0
    for row in data_slice:
        median_price = float(row[61])
        sold = row[62]

        if median_price >= price_range[0] and median_price <= price_range[1]:
            price_slice.append(row)
            if sold == 'Yes':
                sold_count += 1

    try:
        win_rate = sold_count / (len(price_slice) * 1.0)
    except:
        median_price_start += increment
        price_range = [0.95 * median_price_start, 1.05 * median_price_start]
        continue

    # if win_rate >= 0.5 and len(price_slice) >= 25:
    if len(price_slice) >= 25:
        option_range_to_win_rate[(price_range[0], price_range[1])] = {'win rate': win_rate, 'size of slice': len(price_slice)}
    else:
        miss_count += 1

    median_price_start += increment
    price_range = [0.95 * median_price_start, 1.05 * median_price_start]

OUTPUT_FILEPATH = os.path.join(CUSTOMER_ZIPCODE+'_'+JOB_TYPE+'_ideal_price.csv')
with open(OUTPUT_FILEPATH, 'w') as outfile:
    csv_writer = csv.writer(outfile)
    csv_writer.writerow(['price range', 'win rate', 'size of slice'])

    for price_range, data in option_range_to_win_rate.items():
        csv_writer.writerow([price_range, data['win rate'], data['size of slice']])

print('miss count', miss_count)
