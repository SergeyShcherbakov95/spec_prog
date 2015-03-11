__author__ = 'sergey'

import  urllib2
from datetime import datetime
import pandas as pd

def dowl(i):
    index = str(i)
    if i < 10:
        index = '0' + index
    url="http://www.star.nesdis.noaa.gov/smcd/emb/vci/gvix/G04/ts_L1/ByProvince/Mean/L1_Mean_UKR.R" + index + ".txt"
    vhi_url = urllib2.urlopen(url)
    index = str(names[i])
    out = open('vhi-' + index + '-' + datetime.strftime(datetime.now(), "--%m-%Y") + '.csv','wb')
    nameFiles.append('vhi-' + index + '-' + datetime.strftime(datetime.now(), "--%m-%Y") + '.csv')
    out.write(vhi_url.read())
    out.close()
    print "VHI " + index + " is downloaded..."

def readFiles(i):
    df = pd.read_csv('/home/sergey/PycharmProjects/laba1/' + i , index_col = False, header = 1)
    return df

names = {1 : '22', 2: '24', 3 : '23', 4 : '25', 5 : '03', 6 : '04', 7 : '08', 8 : '19', 9 : '20',
            10 : '21', 11 : '09', 13 : '10', 14 : '11', 15 : '12', 16 : '13', 17 : '14', 18 : '15', 19 : '16',
            21 : '17', 22 : '18', 23 : '06', 24 : '01', 25 : '02', 26 : '07', 27 : '05'}

def VHIYearMinMax(df, i, year):
    print "\n"
    print i
    print year
    list =  df.VHI[(df['year'] == year) & (df['VHI'] != -1.00)].tolist()
    print "Year " + str(year) + " VHI_max = " + str(max(list))
    print "Year " + str(year) + " VHI_min = " + str(min(list))

def VHI15(df, i, percent):
    print "\n"
    print i
    print "Max VHI(Area_LESS_15): "
    print df[(df['%Area_VHI_LESS_15'] > percent) & (df['VHI'] < 15)]

def VHI35(df, i, percent):
    print "\n"
    print i
    print "Max VHI(Area_LESS_35): "
    print df[(df['%Area_VHI_LESS_35'] > percent) & (df['VHI'] < 35) & (df['VHI'] > 15)]

def SummerVHI(df, i):
    print "\n"
    print i
    print "Summer: "
    list = df.year[(df['VHI'] > 60) & (df['week'] > 22) & (df['week'] < 27)].tolist()
    for i in list:
        index =  list.count(i)
        if index == 4:
            list.remove(i)
            print i

nameFiles = []

for i in range(1, 28):
    if(i == 12 or i == 20):
        continue
    #dowl(i)
    index = str(names[i])
    nameFiles.append('vhi-' + index + '-' + datetime.strftime(datetime.now(), "--%m-%Y") + '.csv')

for i in nameFiles:
    VHIYearMinMax(readFiles(i), i, 1995)
    VHI15(readFiles(i), i, 1)
    VHI35(readFiles(i), i, 1)
    SummerVHI(readFiles(i), i)
