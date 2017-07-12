'''
@author: Wuil
'''
from crawlerTA import  *
from config import preUrl


def isFinalPage(pageUrl):
    pageUrl = preUrl + pageUrl
    soup = getSoupFromUrl(pageUrl)
    if soup.find('div',{'class':'tcHeader'}) == None:
        return True
    else:
        return False
    
    
    
    

def getFromLocations(locationUrlList):
    vacationList = set()
    locationName = set()
    
    while (len(locationUrlList) >0):
        
        soup = getSoupFromUrl(locationUrlList[0])
        locationUrlList.pop(0)
       
#         print soup
        h1UrlList = soup.findAll('h1')
        h1Url = '' 
        for i in h1UrlList:
            try:
                h1Url = i.a.get('href')
#                 print h1Url
            except:
                continue
#         print h1Url
        
#         h1Url = soup.find('div',{'class':'col poolX adjust_padding new_meta_chevron_v2'})
#         print h1Url
        if isFinalPage(h1Url):
            vacationList.add(h1Url)
#             print h1Url
        countryDiv = soup.find('table')
# print countryDiv
        try:
            tdList = countryDiv.findAll('td')
            for td in tdList:
                try:
                    hyperText = str(td.a.string)
                    hyperLink = td.a.get('href')
                    locationName.add(hyperText)
                    print hyperText
                    if hyperText.startswith('Locations'):
                        locationUrlList.append(preUrl+hyperLink)
                        
                    else:
                        vacationList.add(hyperLink)
    #                     print hyperLink
                        
                except:
                    pass
        except:
            pass
    return [vacationList,locationName]

if __name__ == "__main__":
    url = ['http://www.tripadvisor.com.sg/AllLocations-g186591-Places-Iceland.html']
#     locationList =  getFromLocations(url)
    locationName = getFromLocations(url)[1]
#     print len(locationList)
#     print "locationlist" + locationList
    print locationName
    
