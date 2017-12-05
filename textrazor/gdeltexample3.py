import gdelt
import json

# Version 2 queries
gd2 = gdelt.gdelt(version=2)

# Single 15 minute interval pull, output to json format with mentions table
resultsj = gd2.Search('2016 Nov 1',table='events',output='json')
print(len(resultsj))

# Full day pull, output to pandas dataframe, events table
#results = gd2.Search(['2016 11 01'],table='events',coverage=True)
#print(len(results))

for key in json.loads(resultsj):
    print(key)

