__author__ = 'pramod'

"""
This script will take <n,e,t,d,l> as input for a city and identify events
using the algorithm

ALGORITHM 2:
"""

from pandas import read_csv
from pandas import DataFrame
import datetime as dt
import pandas as pd
import numpy as np
import operator
import matplotlib.pyplot as plt


# supporting methods

def plotallstats(timesteps, numrecords, threshold, freq):
    if freq == "D":
        if threshold == 5:
            plt.subplot(4, 2, 1)
            plt.vlines(timesteps, [0], numrecords, colors='b')
            plt.title('Threshold = ' + threshold.__str__() + ', Granularity = Days')
            plt.ylabel('Number of Events')
        if threshold == 10:
            plt.subplot(4, 2, 3)
            plt.vlines(timesteps, [0], numrecords, colors='g')
            plt.xlabel('Threshold = ' + threshold.__str__())
            plt.ylabel('Number of Events')
        if threshold == 15:
            plt.subplot(4, 2, 5)
            plt.vlines(timesteps, [0], numrecords, colors='r')
            plt.xlabel('Threshold = ' + threshold.__str__())
            plt.ylabel('Number of Events')
        if threshold == 20:
            plt.subplot(4, 2, 7)
            plt.vlines(timesteps, [0], numrecords, colors='c')
            plt.xlabel('Threshold = ' + threshold.__str__())
            plt.ylabel('Number of Events')
    if freq == "W":
        if threshold == 5:
            plt.subplot(4, 2, 2)
            plt.vlines(timesteps, [0], numrecords, colors='b')
            plt.title('Threshold = ' + threshold.__str__() + ', Granularity = Weeks')
            plt.ylabel('Number of Events')
        if threshold == 10:
            plt.subplot(4, 2, 4)
            plt.vlines(timesteps, [0], numrecords, colors='g')
            plt.xlabel('Threshold = ' + threshold.__str__())
            plt.ylabel('Number of Events')
        if threshold == 15:
            plt.subplot(4, 2, 6)
            plt.vlines(timesteps, [0], numrecords, colors='r')
            plt.xlabel('Threshold = ' + threshold.__str__())
            plt.ylabel('Number of Events')
        if threshold == 20:
            plt.subplot(4, 2, 8)
            plt.vlines(timesteps, [0], numrecords, colors='c')
            plt.xlabel('Threshold = ' + threshold.__str__())
            plt.ylabel('Number of Events')

# This function takes a dictionary of <location:count> as input and returns the max of the count
def getmaxcount(loccounts):
    maxloc = 0
    loopcount = 0
    for i in loccounts:
        if loopcount == 0:
            maxloc = loccounts[i]
            loopcount = loopcount + 1
        else:
            if maxloc < loccounts[i]:
                maxloc = loccounts[i]
    return maxloc

# This function will go through the passed rows and find out the majority locations from which
# the tuples have originated
def getmajoritylocations(rows):
    #print rows['location']
    locgrouped = rows.groupby('location')
    dictionary = locgrouped.groups
    locs = dictionary.keys()
    loccounts = dict((i,locs.count(i)) for i in locs)
    maxnum = getmaxcount(loccounts)
    for key, val in loccounts.iteritems():
        if val == maxnum:
            return key

# This function will write a string to a specified file
# event,start_time,end_time,impact,geo_hash_number,lat,long,icon_color
def writetofile(str, filename):
    f = open(filename, 'a')
    f.write(str + ',small_red' + '\n')
    f.close()

#  This function will analyze a time slice
def analyze(vectors, threshold):
    # entities<>event_terms<>day_of_week<>time_of_day<>location<>tweet_text<>time_stamp<>lat<>long
    tuple = vectors[['entities', 'event_terms', 'day_of_week', 'time_of_day', 'location', 'time_stamp','lat','long']]
    types = tuple.groupby('event_terms')
    numtuples = 0
    #print type(types.groups)
    # the groupby results in a dictionary and each entry is a type
    dictionary = types.groups
    for i in dictionary:
        #print i, dictionary[i]
        eventtype = i
        rownums = dictionary[i]
        rows = vectors.loc[rownums]
        #print np.shape(rows)
        majloc = getmajoritylocations(rows)
        starttime = min(rows.iloc[:,6])
        endtime = max(rows.iloc[:,6])
        impact = np.shape(rows)[0]
        lat = rows['location'] == majloc
        selectedrows = rows[lat]
        #print selectedrows['lat'].iloc[0]
        #print selectedrows['long'].iloc[0]
        if impact >= threshold:
            line = eventtype.__str__() + ',' + starttime + ',' + endtime + ',' + impact.__str__() + ',' + majloc.__str__() + ',' + selectedrows['lat'].iloc[0].__str__() + ',' + selectedrows['long'].iloc[0].__str__()
            print line
            writetofile(line, "data/extractedeventsfromtweets.csv")
            numtuples = numtuples + 1
    return numtuples

# Read all the tuples
# entities<>event_terms<>day_of_week<>time_of_day<>location<>tweet_text<>time_stamp<>lat<>long
FILENAME = "data/final-training-data-nov.txt"
df = pd.read_csv(FILENAME, delimiter="<>")
thresholdlist = [10]

# Generate the time stamps for the entire range of time the tweets were generated
print df.iloc[1,6]
print df.iloc[np.shape(df)[0] - 1, 6]

#start = pd.to_datetime('2013-07-30 19:03:27')
#end = pd.to_datetime('2013-08-01 13:00:09')
start = pd.to_datetime(df.iloc[1,6])
end = pd.to_datetime(df.iloc[np.shape(df)[0] - 1, 6])
# this can be later changed to days or any other granularity
# W - weekly, D - Daily, H - Hourly increments
for threshold in thresholdlist:
    for freq in ['D']:
        rng = pd.date_range(start, end, freq=freq)
        #print type(rng)

        # for plotting
        timesteps = []
        numrecords = []

        # slicing the data based on the time stamp
        loopcount = 0
        for timeindex in rng:
            if loopcount == 0:
                stime = timeindex
                loopcount = loopcount + 1
            else:
                etime = timeindex
                print stime, etime
                tmp = df[(df['time_stamp'] > stime.__str__()) & (df['time_stamp'] < etime.__str__())]
                # analyze takes <data> <threshold>
                # threshold indicated the minimum number of tuples required to declare an event
                numtuples = analyze(tmp, threshold)
                #print numtuples
                timesteps.append(loopcount)
                numrecords.append(numtuples)
                #print np.shape(tmp)
                stime = etime
                loopcount = loopcount + 1

        plotallstats(timesteps, numrecords, threshold, freq)

plt.show()
# All the things I tried to get the timestamp based query/filtering working :)


    #print dictionary
    #print max(dictionary.keys())
    #if len(locs) < 2:
    #    return max(dictionary.keys())
    # we will return the maximum of the entries in the list
    #return max(dictionary.keys())

#df['time_stamp'].apply(lambda x: pd.to_datetime(x))

#print np.shape(df)
#df = df[(df['time_stamp'] > '2013-07-30 22:08:06') & (df['time_stamp'] < '2013-07-30 22:13:10')]
#print np.shape(df)

# Select tuples that were reported with a time delta t
# 2013-07-30 19:03:27
# 2013-08-01 13:00:09
#st = dt.datetime(2013, 7, 30, 0, 0)
#en = dt.datetime(2013, 8, 1, 0, 0)
#print type(st)
#print type(en)
#df[df['time_stamp'].apply(lambda x: checkrnage(x, st, en))]
#df['time_stamp'].apply(lambda x: dt.datetime.fromtimestamp(x))

#ts = pd.Series(np.random.randn(len(rng)), index=rng)

#time = timestamps.ix[ts]
#print type(time)
#print np.shape(time)

#dft = pd.DataFrame(df,columns=['time_stamp'],index=rng)
#print type(dft)
#print np.shape(dft)

#rng = pd.date_range('1/1/2000', periods=24, freq='H')
#ts = pd.Series(pd.np.random.randn(len(rng)), index=rng)
#print ts
#ts = ts.ix[ts.index.indexer_between_time('01', '07')]
#print ts
# Assign event type to each tuple
