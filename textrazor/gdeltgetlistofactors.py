import gdelt
import json

# Version 2 queries
gd2 = gdelt.gdelt(version=2)

# Single 15 minute interval pull, output to json format with mentions table
#resultsj = gd2.Search('2016 Nov 1',table='events',output='json')
#print(len(resultsj))

#for key in json.loads(resultsj):
#    print(key)

#Full day pull, output to pandas dataframe, events table
##change date here as needed

results = gd2.Search(['2017-08-26'],table='events',coverage=True)
#print(len(results))

##print list(results.columns.values)
#print results.head(10)

res = results['Actor1Name'].value_counts()
#print res

list1 = res.index.tolist()

##shows top 30 terms for actor1 based on frequency of occurrence
print list1[:30]

df = results.dropna(subset=['Actor1Name'])
df2 = df.dropna(subset=['Actor2Name'])

res = results['Actor2Name'].value_counts()
#print res

list2 = res.index.tolist()

print list2[:30]



#results = gd2.Search(['2017 10 03'],table='mentions',coverage=True)
#print(len(results))

#print list(results.columns.values)

#print results.head(10)
