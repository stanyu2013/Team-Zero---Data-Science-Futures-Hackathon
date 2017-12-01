
import csv
import gdelt
import json
import re

# Version 2 queries
gd2 = gdelt.gdelt(version=2)

datepat=re.compile("201[5-7]-[0-9-]+$")

with open('extracted_dates.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for row in reader:
        name=row[0]
        date=row[1]
        if datepat.match(date):
            print("Video: " + name)
            print("Date:  " + date)
            print("Entities/Actors for that date:")

            results = gd2.Search([date],table='events',coverage=True)
            res = results['Actor1Name'].value_counts()
            list1 = res.index.tolist()
            print list1[:30]
 
            print("")

            df = results.dropna(subset=['Actor1Name'])
            df2 = df.dropna(subset=['Actor2Name'])

            res = results['Actor2Name'].value_counts()
            list2 = res.index.tolist()

            print list2[:30]

            print("--------------------------------------------------------------------")
