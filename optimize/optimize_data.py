import csv
import os

IN_DATAPATH = os.path.join('..', 'dataset', '2019to2021_RandazzoData_without_0_v2.csv')

OPTIMIZED_DATAPATH = os.path.join('..', 'dataset', 'bucketed_2019to2021_RandazzoData_without_0_c2.csv')

CURR_YEAR = 2021

CAMPAIGN_BUCKETS = {
                    'traditional media': ['Channel 2', 'Channel 4', 'Channel 7', 'Charity Ads', 'Comcast', 'dBusiness Magazine', 'Detroit Home Magazine', 'Early Bird Spring Maintenance', 'Hager Fox TV', 'Home Show - Fall', 'Home Show - Spring', 'Home Show - Winter', 'Letter', 'Novi Home Show', 'Radio', 'Showroom Walk-in', 'TV', 'Yard Sign', 'Randazzo Apparel', 'Truck', 'Callfire Texts'],
                    'referrals': ['Referral', 'Referral - Consumers', 'Referral - Employee', 'Referral - Friend', 'Referral - Rinnai Tankless', 'Referral - Service Tech', 'Referral - Unico'],
                    'return customer': ['Existing Customer', 'Existing Maintenance Member', 'Return Customer', 'Furnace Sticker'],
                    'online': ['Angie\'s List - Ran', 'Google', 'Google - HF', 'Online Listing', 'Price/Pass Email', 'Social Media', 'Web Store', 'Website', 'Website Bookings', 'Yelp', 'Yelp Integration']
                    }

def get_new_campaign(campaign):
    if campaign in CAMPAIGN_BUCKETS['traditional media']:
        return 'traditional media'
    elif campaign in CAMPAIGN_BUCKETS['referrals']:
        return 'referral'
    elif campaign in CAMPAIGN_BUCKETS['return customer']:
        return 'return customer'
    elif campaign in CAMPAIGN_BUCKETS['online']:
        return 'online'
    else:
        return 'other'

def get_na_count(row):
    na_count = 0

    job_type = row[0]
    if job_type == 'NB':
        na_count += 1

    campaign = row[1]
    if campaign == 'NB':
        na_count += 1

    correctESvsEG = row[3]
    if correctESvsEG == '0':
        na_count += 1

    loan_amount = row[6]
    if loan_amount == '162000':
        na_count += 1

    sale_price = row[7]
    if sale_price == '168362.5':
        na_count += 1

    value = row[8]
    if value == '247000':
        na_count += 1

    basement = row[12]
    if basement == 'NA':
        na_count += 1

    stories = row[13]
    if stories == '1.31':
        na_count += 1

    year_built = row[14]
    if year_built == '1969':
        na_count += 1

    sq_ft = row[15]
    if sq_ft == '1873':
        na_count += 1

    return na_count

with open(IN_DATAPATH, 'r') as infile:
    with open(OPTIMIZED_DATAPATH, 'w') as outfile:
        rows = csv.reader(infile)
        variables = next(rows)
        new_variables = variables
        new_variables[14] = 'house age'

        csv_writer = csv.writer(outfile)
        csv_writer.writerow(new_variables + ['NA count'])

        for row in rows:
            # count how many NA/medians are in the row
            na_count = get_na_count(row)
            if na_count >= 6:
                continue

            # bucket certain values together for campaigns
            campaign = row[1]
            new_campaign = get_new_campaign(campaign)

            # change `year built` to `house age`
            year_built = row[14]
            house_age = CURR_YEAR - int(year_built)

            new_row = row
            new_row[1] = new_campaign
            new_row[14] = house_age

            csv_writer.writerow(new_row + [na_count])
