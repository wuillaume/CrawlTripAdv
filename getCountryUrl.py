'''
@author: Wuil
'''

from crawlerTA import getSoupFromUrl

url = 'http://www.tripadvisor.com.sg/AllLocations-g1-Places-World.html'
soup = getSoupFromUrl(url)
targetList = ["greece","nepal","hungary","cayman islands","honduras",\
              "pakistan","cuba","grenada","greenland","iceland","saudi arabia","sri lanka","india","philippines"]
#"maldives","cambodia","mauritius","bhutan",\              "serbia"
#add japan

countryDict = {}

countryDiv = soup.find('table')
# print countryDiv
tdList = countryDiv.findAll('td')
for td in tdList:
    try:
        print td.a.string[13:]+"\t"+td.a.get('href')
        countryDict[(td.a.string[13:]).lower()] = td.a.get('href')
    except:
        pass

def listLinkCountries():
    countryDiv = soup.find('table')
    # print countryDiv
    tdList = countryDiv.findAll('td')
    for td in tdList:
        try:
            print td.a.string[13:]+"\t"+td.a.get('href')
            countryDict[(td.a.string[13:]).lower()] = td.a.get('href')
        except:
            pass
    return countryDict
    
for i in targetList:
    if i in countryDict:
        print i+'\t'+countryDict[i]
