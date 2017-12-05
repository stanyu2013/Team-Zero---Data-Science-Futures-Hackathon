import gdelt
import json



def correlation(x, y):
    # evaluate the correlation coefficient and p-value of two variables x and y

    import scipy.stats as st

    # correlation coefficient r and (two-tailed) p-value
    r, p = st.pearsonr(x, y)

    return r, p




# Version 2 queries
gd2 = gdelt.gdelt(version=2)

# Single 15 minute interval pull, output to json format with mentions table
#resultsj = gd2.Search('2016 Nov 1',table='events',output='json')
#print(len(resultsj))

#for key in json.loads(resultsj):
#    print(key)



#Full day pull, output to pandas dataframe, events table
results = gd2.Search(['2017 10 05'],table='events',coverage=True)
#print(len(results))

print list(results.columns.values)
#print results.head(10)

res1 = results['Actor1Name'].value_counts()
print res1

df = results.dropna(subset=['Actor1Name'])

res2 = results['Actor2Name'].value_counts()
print res2


#results = gd2.Search(['2017 10 03'],table='mentions',coverage=True)
#print(len(results))

#print list(results.columns.values)

#print results.head(10)


print(res1[0])
print(res1[0, 0])

x = []
y = []
for i in range(len(res1)):
    for j in range(len(res2)):
        if res1.at[i] == res2.at[j]:
            x.append(res1.at[i].at[0])
            y.append(res2.at[j].at[0])
            break
print(x)
print(y)


r, p = correlation(x, y)
print('the correlation coefficient: ')
print(r)

