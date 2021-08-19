import os
import csv
import datetime
import requests
import json

# firstname, lastname, and address are required
# city & state are optional if postal code is used
# zip code is optional if city & state are used

LICENSE_KEY = '8e648b02-f052-4acd-b3a1-15284eff308c'
curr_yr = datetime.datetime.now().year
URL_FIRST_HALF = 'https://api.accurateappend.com/Services/V2/AppendDob/'+LICENSE_KEY+'/?'

def get_name(row):
    name = row[0]
    if '&' in name and len(name.split()) == 4:
        first_name1 = name.split()[0]
        first_name2 = name.split()[2]
        last_name = name.split()[3]
    elif len(name.split()) == 2:
        first_name1 = name.split()[0]
        first_name2 = None
        last_name = name.split()[1]
    else:
        first_name1 = None
        first_name2 = None
        last_name = None

    return first_name1, first_name2, last_name

def get_location(row):
    address = row[1].replace(' ', '%20')
    city = row[2].replace(' ', '%20')
    state = row[3]
    zip = row[4]

    return address, city, state, zip

def get_response(first_name, last_name, address, city, state, zip):
    if first_name1 and last_name and address and city and state and zip:
        response = requests.get(URL_FIRST_HALF+'firstname='+first_name1+'&lastname='+last_name+'&address='+address+'&city='+city+'&state='+state+'&postalcode='+zip)
    elif first_name1 and last_name and address and city and state:
        response = requests.get(URL_FIRST_HALF+'firstname='+first_name1+'&lastname='+last_name+'&address='+address+'&city='+city+'&state='+state)
    elif first_name1 and last_name and address and zip:
        response = requests.get(URL_FIRST_HALF+'firstname='+first_name1+'&lastname='+last_name+'&address='+address+'&postalcode='+zip)
    else:
        return None

    return response

def response_is_successful(response):
    if response and response.status_code == 200:
        response = response.json()
        if 'Dob' in response and response['Dob']['MatchLevel'] == 'E1':
            try:
                dob = int(response['Dob']['Dob'][:4])
                return True
            except:
                return False

    return False

with open(os.path.join('..', 'dataset', 'internal+estated+dist+incomes.csv'), 'r') as infile:
    with open(os.path.join('..', 'dataset', 'internal+estated+dist+incomes+age.csv'), 'w') as outfile:
        in_rows = csv.reader(infile)
        in_variables = next(in_rows)

        csv_writer = csv.writer(outfile)
        csv_writer.writerow(in_variables + ['age'])

        row_i = 0
        for row in in_rows:
            # extract info from row
            first_name1, first_name2, last_name = get_name(row)
            address, city, state, zip = get_location(row)

            # call API
            response = get_response(first_name1, last_name, address, city, state, zip)

            # check validity of response
            if response_is_successful(response):
                dob = int(response.json()['Dob']['Dob'][:4])

            # if response not valid, try the second first name
            else:
                # call API
                response = get_response(first_name2, last_name, address, city, state, zip)

                # check validity of response
                if response_is_successful(response):
                    dob = int(response.json()['Dob']['Dob'][:4])

                # unable to find dob, write 'NA' to row and move on
                else:
                    csv_writer.writerow(row + ['NA'])
                    continue

            # dob was found, write person's age to the row
            csv_writer.writerow(row + [curr_yr - dob])
            print(curr_yr - dob, row_i, (row_i / 35242.0) * 100, '%')
