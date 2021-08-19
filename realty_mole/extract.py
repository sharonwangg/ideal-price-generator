import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import numpy as np

url = "https://realty-mole-property-api.p.rapidapi.com/properties"

# Good for given a number of parameters of "good attributes" that the model
# determines, returns a list of possible future desirable customers

# Can also extract external data on the house's age by accessing the `yearBuilt`ß
# column, # of bedrooms, # of bathrooms, county, property type (apt, single family, condo, etc),
# square footage, etc

# Can specify:
# limit (max number of records to return)
# city, # of bedrooms, latitude, state, # of bathrooms,
# radius from address/latitude/longitude, longitude, address

# Note: sometimes specific addresses don't show up (not all addresses in database)
querystring = {"limit":"10","city":"Cincinnati","bedrooms":"3","state":"OH","bathrooms":"2"}

headers = {
    'x-rapidapi-key': "INSERT API KEY HERE",
    'x-rapidapi-host': "realty-mole-property-api.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)
df = pd.DataFrame(response.json())
df.to_excel (r'response.xlsx', index=False, header=True)
