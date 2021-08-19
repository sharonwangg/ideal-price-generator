import requests
import json
import csv

TOKEN = 'INSERT TOKEN HERE'

# street_address = '11166 Shadow Creek Court'
# city = 'Sterling Heights'
# state = 'MI'
# zip_code = '48313'
#
# response = requests.get('https://apis.estated.com/v4/property?token='+TOKEN+'&street_address='+street_address+'&city='+city+'&state='+state+'&zip_code='+zip_code)
#
# print(response.json().get('data', 'NA'))
#
# quit()

with open('new_data.csv', 'w') as outfile:
    with open('extracted_randazzo_estimates.csv', 'r') as infile:
        # creating a csv reader object
        in_rows = csv.reader(infile)

        # creating a csv writer object
        csv_writer = csv.writer(outfile)

        # extracting field names through first row
        in_fields = next(in_rows)

        out_fields = in_fields + ['latitude', 'longitude', 'area_sq_ft', 'zoning', 'year_built', 'effective_year_built', 'stories', 'rooms_count', 'heating_type', 'heating_fuel_type', 'air_conditioning_type', 'value', 'sale_price', 'loan_due_date', 'loan_amount']

        csv_writer.writerow(out_fields)

        i = 0
        # going through each data row one by one
        for in_row in in_rows:
            i += 1
            if in_row[10] == 'Completed':
                street_address = in_row[1]
                city = in_row[2]
                state = in_row[3]
                zip_code = in_row[4]

                response = requests.get('https://apis.estated.com/v4/property?token='+TOKEN+'&street_address='+street_address+'&city='+city+'&state='+state+'&zip_code='+zip_code)

                house = response.json().get('data', 'NA')
                if house != 'NA' and response.status_code == 200 and house is not None:
                    print('row '+str(i)+', '+str(100 * float(i/35243.0))+'%')
                    address = house.get('address', 'NA')
                    if address == 'NA' or address is None:
                        latitude = 'NA'
                        longitude = 'NA'
                    else:
                        latitude = address.get('latitude', 'NA')
                        longitude = address.get('longitude', 'NA')

                    parcel = house.get('parcel', 'NA')
                    if parcel == 'NA' or parcel is None:
                        area_sq_ft = 'NA'
                        zoning = 'NA'
                    else:
                        area_sq_ft = parcel.get('area_sq_ft', 'NA')
                        zoning = parcel.get('zoning', 'NA')

                    structure = house.get('structure', 'NA')
                    if structure == 'NA' or structure is None:
                        year_built = 'NA'
                        effective_year_built = 'NA'
                        stories = 'NA'
                        rooms_count = 'NA'
                        heating_type = 'NA'
                        heating_fuel_type = 'NA'
                        air_conditioning_type = 'NA'
                    else:
                        year_built = structure.get('year_built', 'NA')
                        effective_year_built = structure.get('effective_year_built', 'NA')
                        stories = structure.get('stories', 'NA')
                        rooms_count = structure.get('rooms_count', 'NA')
                        heating_type = structure.get('heating_type', 'NA')
                        heating_fuel_type = structure.get('heating_fuel_type', 'NA')
                        air_conditioning_type = structure.get('air_conditioning_type', 'NA')

                    valuation = house.get('valuation', 'NA')
                    if valuation == 'NA' or valuation is None:
                        value = 'NA'
                    else:
                        value = valuation.get('value', 'NA')

                    deeds = house.get('deeds', 'NA')
                    if deeds == 'NA' or deeds is None or len(deeds) == 0:
                        sale_price = 'NA'
                        loan_due_date = 'NA'
                        loan_amount = 'NA'
                    else:
                        sale_price = deeds[0].get('sale_price', 'NA')
                        loan_due_date = deeds[0].get('loan_due_date', 'NA')
                        loan_amount = deeds[0].get('loan_amount', 'NA')

                    out_row = in_row + [latitude, longitude, area_sq_ft, zoning, year_built, effective_year_built, stories, rooms_count, heating_type, heating_fuel_type, air_conditioning_type, value, sale_price, loan_due_date, loan_amount]

                else:
                    out_row = in_row + ['NA', 'NA', 'NA', 'NA',
                                        'NA', 'NA', 'NA', 'NA',
                                        'NA', 'NA', 'NA', 'NA',
                                        'NA', 'NA', 'NA']

            csv_writer.writerow(out_row)
