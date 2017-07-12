import httplib
import urllib
import urllib2 
import re
import csv
from csv import DictReader
from sys import argv
import sys
import os
import subprocess
import webbrowser
from cookielib import CookieJar
import time
from getFromLocations import getFromLocations
import getCountryUrl


def readCountries(nameFile):
    with open(nameFile, 'rb') as csvfile:    
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        l= []
        for row in spamreader:
            #row = " ".join(row)
            
            url = "http://www.google.com/trends/trendsReport?cat=0-67&q=" + "%20".join(row) +'&export=1'
            print url
            l.append(url)
            #target = open(" ".join(row), 'w')        
           # target.truncate()
            #r.download_report((row))
            #target.write(r.raw_data)
            #target.close()
            #print r.raw_data.split('\n\n\n')
        return l

def readLocations(loclist):
    l= []
    for row in loclist:
        #row = " ".join(row)
        print "unchanged : " + row
        if "Locations in" in row:
            row = row.split(" ")
            le = len(row)
            res = ""
            for i in range(2,le):
                if i>2:
                    res = res +"%20"
                res = res+ row[i]
            row=res
            print "changed :" + row
#         if row.find(" "):
#             row= "%20".join(row)
        link = "http://www.google.com/trends/trendsReport?cat=0-67&q=" + row +'&export=1'
        print link
        l.append(link)
    return l
    
def all_files(directory):
    for path, dirs, files in os.walk(directory):
        for f in files:
            yield os.path.join(path, f)

# r3d_files = [f for f in all_files('C:\Users\user\Documents\NUS\Courses NUS\IS5126\GoogleTrend\downMoz')
#                if f.endswith('.csv')]
# print r3d_files
    
def renameDownload(directory,countryName):
    for f in all_files(directory):
        
        if 'report' in f:
            with open(f, 'rb') as csvfile:    
                csvread = csv.reader(csvfile, delimiter=':', quotechar='|')
                row = csvread.next()
            print(row[len(row)-1])
            try:
                os.rename(f,directory+ '\\changed\\'+countryName+"_"+row[len(row)-1]+'.csv')
                print f + 'renamed in' + directory+ '\\changed\\'+countryName+"_"+row[len(row)-1]+'.csv'
            except:
                os.remove(f)
                print "remove " + f
                pass
            
            
    
def openUrl(url):
    if sys.platform=='win32':
        os.startfile(url)
        os.chdir("file:///home/chronos/user/downloads/1")
    elif sys.platform=='darwin':
        subprocess.Popen(['open', url])
    else:
        try:
            subprocess.Popen(['xdg-open', url])
        except OSError:
            print 'Please open a browser on: '+url

# certainFolder = '.'
# allR3DFiles = filesByPattern(certainFolder, lambda fn: fn.endswith('.R3D'))

count = 0                
# renameDownload('C:\Users\user\Documents\NUS\Courses NUS\IS5126\GoogleTrend\downMoz')
urls = ['http://www.tripadvisor.com.sg/AllLocations-g189952-Places-Iceland.html']
urls = getCountryUrl.listLinkCountries()
print urls
for i in getCountryUrl.targetList:
    if i in urls:
        
        url = 'http://www.tripadvisor.com.sg/'+urls[i]
        
        temp = url.split("Places-")
        countryName = temp[len(temp)-1][:-5]
        #     locationList =  getFromLocations(url)
        # locationName = getFromLocations(url)[1]
        location = getFromLocations([url])[1]
        print location
        locationUrl = readLocations(location)
        for elem in locationUrl:
           
               
            url = elem
            count = count+1
            if(count==50):
                time.sleep(60)
                renameDownload('C:\Users\user\Documents\NUS\Courses NUS\IS5126\GoogleTrend\downChrom',countryName)
                time.sleep(60)
                count=0   
            print count
            if sys.platform=='win32':
                os.startfile(url)
            elif sys.platform=='darwin':
                subprocess.Popen(['open', url])
            else:
                try:
                    subprocess.Popen(['xdg-open', url])
                except OSError:
                    print 'Please open a browser on: '+url
    renameDownload('C:\Users\user\Documents\NUS\Courses NUS\IS5126\GoogleTrend\downChrom',countryName)

#webbrowser.open_new('http://www.google.com/trends/trendsReport?cat=0-67&q=New%20Zealand&export=1')