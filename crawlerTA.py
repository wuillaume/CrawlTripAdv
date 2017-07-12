'''
Created on Mar 10, 2015
@copyright: ALl Rights Reserved 2015
@author: Wuil
@organization: National University of Singapore
@version: 0.1 
'''
import sys,re,time,os
from config import *
import urllib2
from ast import literal_eval
import string
from bs4 import BeautifulSoup
from config import *
from getFromLocations import *

jobidList = []
preUrl = 'http://www.tripadvisor.com.sg/'
def playerUrls():
    playerUrlsList = []
    preUrl = 'http://www.basketball-reference.com/players/'
    az = string.lowercase[0:26]
    for i in range(26):
        playerUrlsList.append(preUrl+az[i]+'/')
        print preUrl+az[i]+'/'
        
    return playerUrlsList

def teamsUrl():
    teamUrl = 'http://www.basketball-reference.com/teams/'
    return teamUrl
    
def getSoupFromUrl(url):
    time.sleep(0.5)
#     req = urllib2.Request(url, headers={'User-Agent' : " Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)"})
    req = urllib2.Request(url, headers={'User-Agent' : " Mozilla/4.0(compatible; MSIE 7.0b; Windows NT 6.0)",'Accept-Language':'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4'}) 
    webpage = urllib2.urlopen(req)
    soup = BeautifulSoup(webpage.read(),from_encoding="utf-8")
    return soup

def getSoupFromStr(webpageStr):
    soup = BeautifulSoup(webpageStr)
    return soup

def getWebPage(url):
#     time.sleep(1)
    req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
    webpage = urllib2.urlopen(req)
    return webpage
    
    
def crawlForTeamNames(soup):
   
#     soup = getSoupFromUrl(url)
    
    nbaTeamNamesList = []
    
    for item in soup.findAll('div',{'class':'stw'}):
        if item.findAll('div',{'class','table_heading'})[0].h2.string=='Active Franchises':
#             teamName = item.findAll('div',{'class','table_heading'})[0].h2.string 
#             print  teamName
            
            for i in item.findAll('tr',{'class':'full_table'}):
                teamName = i.a.get('href')
                print teamName
                nbaTeamNamesList.append(teamName)
    return nbaTeamNamesList

def crawlForTeamDetail(soup):
#     soup = getSoupFromUrl(url)
    info = soup.find('table',{'class':'sortable  stats_table'})
    teamInfoList = []
    for tr in info.findAll('tr'):
        seasonInfo = []
        for td in tr.findAll('td'):
            tdInfo = ''
            
            if td.a!=None:
                if td.a.stirng == '':
                    tdInfo = 'None'
                else:
                    tdInfo = td.a.string
                        
#                         print j.a.string
            else:
                if td.string==None:
                    tdInfo = 'None'
                else:
                    tdInfo = td.string
            seasonInfo.append(tdInfo)
        if seasonInfo!=[]: 
            print seasonInfo
            teamInfoList.append(seasonInfo)
    return teamInfoList

def crawlForPlayerNames(nameUrlList):
    playerInfoList=[]
    infoList =[]
#     nameUrlList = ['http://www.basketball-reference.com/players/a']
    for url in nameUrlList:
        soup = getSoupFromUrl(url)
        for item in soup.findAll('table',{'class':'sortable  stats_table'}):
#             for i in item.findAll('th',{'class':'tooltip sort_default_asc'}):
#                 headList.append(i.string)
#                 print i.string
#             i = None
            for i in item.findAll('tr'):
                for j in i.findAll('td'):
#                     print j.a.string
#                     infoList.append(j.a.string)
                    if j.a!=None:
                        if j.a.stirng == '':
                            infoList.append('None')
                        else:
                            infoList.append(j.a.string)
                        infoList.append(j.a.get('href'))
                        
#                         print j.a.string
                    else:
                        if j.string == None:
                            infoList.append('None')
                        else:
                            infoList.append(j.string)
#                         print j.string
                        
                if infoList!=[]:
                    playerInfoList.append(infoList)
                infoList=[]
    return playerInfoList
                
def crawlForPlayerDetail(soup):
#     print url
    resultList = []
#     soup = getSoupFromUrl(url)
    
    #get the draft data
    basicInfo = soup.find('div',{'class':'overflow_auto width100'}).findAll('p',{'class':'padding_bottom_half'})
    for i in basicInfo:
        resultList.append(str(i))
    draftInfo = getDraftInfo(''.join(resultList))
#     print draftInfo
    
    perfmList = []
    salaryList = []
    
    #get the total performance data
    totalInfo = soup.find('div',{'class':'stw','id':'all_totals'})
    for item in totalInfo.findAll('tr'):
        rowList = []
        tdInfo = item.findAll('td')
        if len(tdInfo) == 30: 
            for td in item.findAll('td'):
                if td.string == None:
                    rowList.append('None')
                else:
                    rowList.append(td.string)
            if rowList[0] != 'None':
                perfmList.append(rowList)
#     for i in perfmList:
#         print i

    #get the salary data
    try:
        salaryInfo = soup.find('div',{'class':'stw','id':'all_salaries'})
        for item in salaryInfo.findAll('tr'):
            rowList = []
            for td in item.findAll('td'):
    #                 print td.string
                if td.string == None:
                    rowList.append('None')
                else:
                    rowList.append(td.string)
    #             print rowList
            if rowList and rowList[0] != 'None':
                salaryList.append(rowList)  
    #         for i in salaryList:
    #             print i
    except:
        pass
            
    return [draftInfo,perfmList,salaryList]

            
        
        
def getDraftInfo(inputStr):
    draftPattern = r'(?<=<br><span class="bold_text">Draft:</span>).*'
    draftPattern2 = r'(?<=</a>,)[^<]*'
    draftPattern3 = r'(?<=/draft/)[^\.]*' 
    draftPattern4 = r'(?<=,).*(?= )'  
    
#     print tempStr
    try:
        patternTemp = re.compile(draftPattern)
        tempStr = patternTemp.findall(inputStr)[0]
        draftOrderTemp = re.compile(draftPattern2).findall(tempStr)[0].strip()[:-1]
        draftOrder = re.compile(draftPattern4).findall(draftOrderTemp)[0].strip()
        draftYear = re.compile(draftPattern3).findall(tempStr)[0].strip()
        if draftOrder == '':
            draftOrder = 'None'
        if draftYear == '':
            draftYear = 'None'
        return ([draftOrder,draftYear])
    except:
        return['None','None']   
        
                
class Player:
    basicInfo =[]
    performanceInfo =[]
    salaryInfo = []
    
    def __init__(self):
        pass
    def toString(self):
        pass
        
       
def getNameList(file_path):
    resultList = []
    f = open(file_path,'r')
    while True:
        line = f.readline()
        if not line:
            break
        items = line.strip().split('\t')
#         name = items[0]
#         url = playersPreUrl+str(items[1])
        resultList.append(items)
    
    f.close()
    return resultList
def getRawPage():
#     f = open('../rawData/players/playerDetail','a')
    infoList = getNameList('../data/players/playerInfo')
    for i in infoList[4110  :]:
        print infoList.index(i)
        name = i[1].split('/')[-1]
        print name
        f = open('../data/rawData/players/'+name,'w')
        time.sleep(1.1)
        
        url = playersPreUrl+str(i[1])
        req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
        webpage = urllib2.urlopen(req)
        pageInfo = webpage.read()
        
        f.write(str(pageInfo))
        f.close()

def loadData(input_filePath):
    
    f = open(input_filePath,'r')
    while True:
        line = f.readline()
        if not line:
            break
        line = line.strip()
        print line
        input_line = literal_eval(line)
        print ','.join(input_line[0]+input_line[1])
    f.close()
def getNationality(inputStr):
    
#     nationPattern = r'(?<=margin_left flag).*(?=")'
    try:
        nationPattern = r'(?<=birthplaces\.cgi\?country=).*(?=&)'
        nation = re.compile(nationPattern).findall(inputStr)[0]
        return nation.strip()
    except:
        return 'None'
    

def getTwitterInfo(inputStr):
    tUrl = ''
    follwersNum = 0
    twitterPreUrl = 'https://twitter.com/'
    tPattern = r'https://twitter.com/[^"]*'
    try:
        tUrl = re.compile(tPattern).findall(inputStr)[0].split('/')[-1]
        tUrl = twitterPreUrl+tUrl
        
        
#         print tUrl
#         tUrl = 'https://twitter.com/@KDTrey5'
        req = urllib2.Request(tUrl, headers={'User-Agent' : "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}) 
        webpage = urllib2.urlopen(req)
        soup = BeautifulSoup(webpage.read())
        divInfo =  soup.find('div',{'class':'ProfileNav'})
        liInfo = divInfo.find('li',{'class':'ProfileNav-item ProfileNav-item--followers'})
        follwersNum = liInfo.a.get('title')[0:-10].replace(',','')
#         soup = getSoupFromUrl(tUrl)
#         f.write(soup)
#         print soup
    except:
        return ['None','None']
#     followerInfo = soup.findall('ul',{'class':'ProfileNav-list'})
#     print followerInfo
    
    return [tUrl,follwersNum]
    
def getFromLocal():
    folderPath = '../data/rawData/players/'
#     fileList = os.listdir(folderPath)
    g = open('../data/players/playerDetail2.0part','w')
    
    infoList = getNameList('../data/players/playerInfo')
    for i in infoList[:986]:
#         time.sleep(0.8)
        finalResultList =[]
#         url = playersPreUrl+str(i[1])
        print i[0], infoList.index(i)
        fileName = str(i[1].split('/')[-1])
#         print fileName
        f = open(folderPath+fileName,'r')
        webpage = ''
        while True:
            line = f.readline()
            if not line :
                break
            webpage += (line)
        f.close()
        soup = getSoupFromStr(webpage)
        
        result = crawlForPlayerDetail(soup)
#         nationInfo = getNationality(webpage)
        
        finalResultList.append(i)
#         result.append(nationInfo)
        finalResultList += result
        
        nationInfo = getNationality(webpage)
        finalResultList.append([nationInfo])
        
        twitterInfo = getTwitterInfo(webpage)
        finalResultList.append(twitterInfo)
        uniqID = fileName[:-5]
        finalResultList.insert(0, uniqID)
        
        print finalResultList
        g.write(str(finalResultList))
        g.write('\n')
#     
    g.close()
     
  
    
#     for file in fileList[0:1]:
#         finalResult =[]
#         file = 'duranke01.html'
#         f = open(folderPath+file,'r')
#         webpage = ''
#         while True:
#             line = f.readline()
#             if not line :
#                 break
#             webpage += (line)
#         f.close()
#         soup = getSoupFromStr(webpage)
#         crawlForPlayerDetail(soup)
#         print getNationality(webpage)
#         print getTwitterInfo(webpage)
# #         print getDraftInfo(webpage)
#         
 
def getSimilarityFromLocal():
    folderPath = '../data/rawData/players/'
#     fileList = os.listdir(folderPath)
    g = open('../data/players/similarity','w')
    
    infoList = getNameList('../data/players/playerInfo')
    for i in infoList[0:]:
#         time.sleep(0.8)
        finalResultList =[]
#         url = playersPreUrl+str(i[1])
        print i[0], infoList.index(i)
        fileName = str(i[1].split('/')[-1])
#         print fileName
        f = open(folderPath+fileName,'r')
        webpage = ''
        while True:
            line = f.readline()
            if not line :
                break
            webpage += (line)
        f.close()
        soup = getSoupFromStr(webpage)
        
        try:
            tbodyInfo = soup.find('div',{'class':'table_container','id':'div_sim_career'}).find('tbody')
            simList =[]
            simPlayerInfo =[fileName]
            for tr in tbodyInfo.findAll('tr'):
                
                    tdInfo = tr.findAll('td')[:2]
                    if tdInfo[0].a != None:
                        sName = tdInfo[0].a.string
                        sUrl = tdInfo[0].a.get('href').split('/')[-1][:-5]
                        sim = tdInfo[1].string
    #                     print sName, sUrl, sim
                        simPlayerInfo.append([sName,sUrl,sim])
        except:
            continue
        print simPlayerInfo
     
        g.write(str(simPlayerInfo))
        g.write('\n')
# #     
    g.close()
         

def getList(listUrl, type=None):
    print listUrl
    reviewPageList = []
    soup = getSoupFromUrl(listUrl)
#     hotelSoup = soup.findAll('div',{'class':'listing wrap reasoning_v5_wrap jfy_listing p13n_imperfect'})
    try:
        pageNo = int(soup.findAll('a',{'class':'paging taLnk '})[-1].string)
    except:
        pageNo = 1
#     print pageNo
    pageList = [listUrl]
    
    for i in range(1,pageNo):
        newListUrl = listUrl[:45]+'-oa'+str(i*30)+listUrl[45:]
        pageList.append(newListUrl)
        
    for pu in pageList:
        soup = getSoupFromUrl(pu)
#         print soup
        reviewSoupList = soup.find('div',{'class':'hotels_list_placement'}).findAll('div',{'class':'listing_rating'})
#         print reviewSoupList
        for i in reviewSoupList:
#             print i
            try:
                reviewUrl = i.find('span',{'class':'more'}).a.get('href')
                print reviewUrl
                reviewPageList.append(reviewUrl)
            except:
                pass
         
    return reviewPageList

# def getReviewPage(urlList):
#     reviewUrlList = []
#     for url in urlList:
#         soup = getSoupFromUrl(url)
        
def getReviewPageList(firstPageUrl):
    soup  = getSoupFromUrl(firstPageUrl)
#     reviewCnt = soup.find('a',{'class':'review_count'}).string.strip()
#     reviewCnt = int(str(reviewCnt[:-8]).replace(',',''))
    
    reviewCnt = soup.find('h3',{'class':'reviews_header'}).string.strip()
    reviewCnt = int(str(reviewCnt).split(' ')[0].replace(',',''))
    
    reviewPageList = [firstPageUrl]
    
    
    for i in range(1,int(reviewCnt/10)+1):
#     for i in range(1,2):
        pageUrl =  firstPageUrl[:67]+'-or'+str(i*10)+firstPageUrl[67:]
        print pageUrl
        reviewPageList.append(pageUrl)
        
    return reviewPageList
        
        
        
    
    
def reviewParser(pageUrl):
    soup = getSoupFromUrl(pageUrl)
#     f = open('test','w')
#     f.write(str(soup))
#     print soup
#     print soup
    reviewDiv = soup.findAll('div',{'class':'reviewSelector '})
#     reviewDiv = soup.findAll('div',{'class':'review basic_review inlineReviewUpdate provider0'})
#     print reviewDiv
#     print reviewDiv
    return '\n'.join(str(r) for r in reviewDiv)
    
    
    
def vocationPage(vUrl):
    vUrl = preUrl +vUrl
    soup  = getSoupFromUrl(vUrl)    
    
    print vUrl
    divLink = soup.find('div',{'class':'navLinks'})
    toDoList = {}
#     print divLink
    try:
        hotelUrl = divLink.find('li',{'class':'hotels twoLines'}).a.get('href')
        toDoList['hotel'] = (hotelUrl)
    except:
        pass
    try:
        attractionUrl = divLink.find('li',{'class':'attractions twoLines'}).a.get('href')
#         toDoList['attraction'] = attractionUrl
        
    except:
        pass
    
    try:
        restaurantUrl = divLink.find('li',{'class':'restaurants twoLines'}).a.get('href')
#         toDoList['restaurantUrl'] = restaurantUrl
    except:
        pass
        
#     print hotelUrl, attractionUrl, restaurantUrl

    if 1:
#     for todoUrl in toDoList:
        todoUrl = toDoList['hotel']
        reviewUrlList = getList(preUrl+todoUrl)
        prefileName = '../data/reviews/'
        
        for reviewUrl  in reviewUrlList:
            fileName =  prefileName+reviewUrl[1:-13]
            print fileName
            f = open(fileName,'w')
            reviewPageList = getReviewPageList(preUrl+reviewUrl)
            for pageUrl in reviewPageList: 
                f.write(str(reviewParser(pageUrl))+'\n')
            f.close()
if __name__ == "__main__":
#     url = ['http://www.tripadvisor.com.sg/AllLocations-g186591-Places-Ireland.html']
#     url = ['http://www.tripadvisor.com.sg//AllLocations-g293860-Places-India.html']
#     locationList =  getFromLocations(url)
#     print locationList
#     print len(locationList)
#     locationList = ['/Tourism-g186633-County_Roscommon_Western_Ireland-Vacations.html']
    locationList = set([u'/Tourism-g3649309-Ilam_Bazar_West_Bengal-Vacations.html', u'/Tourism-g2285320-Medak_Telangana-Vacations.html', u'/Tourism-g2282386-Nongpoh_Meghalaya-Vacations.html', u'/Tourism-g424922-Bodh_Gaya_Bihar-Vacations.html', u'/Tourism-g2531447-Lawngtlai_Mizoram-Vacations.html', u'/Tourism-g297670-Rajsamand_Rajasthan-Vacations.html', u'/Tourism-g2289038-Srikakulam_Andhra_Pradesh-Vacations.html', u'/Tourism-g1207703-Majuli_Assam-Vacations.html', u'/Tourism-g3383710-Sirsa_Haryana-Vacations.html', u'/Tourism-g2285308-Mon_Nagaland-Vacations.html', u'/Tourism-g662321-Jamshedpur_Jharkhand-Vacations.html', u'/Tourism-g2288605-Simdega_Jharkhand-Vacations.html', u'/Tourism-g659795-Yanam_Union_Territory_of_Pondicherry-Vacations.html', u'/Tourism-g2287454-Barasat_West_Bengal-Vacations.html', u'/Tourism-g2287463-Banswara_Rajasthan-Vacations.html', u'/Tourism-g2295130-Vythiri_Wayanad_District_Kerala-Vacations.html', u'/Tourism-g312683-Dungarpur_Rajasthan-Vacations.html', u'/Tourism-g858474-Tezpur_Assam-Vacations.html', u'/Tourism-g1584824-Palia_Uttar_Pradesh-Vacations.html', u'/Tourism-g1155908-Rajahmundry_Andhra_Pradesh-Vacations.html', u'/Tourism-g670892-Gingee_Tamil_Nadu-Vacations.html', u'/Tourism-g3783112-Thiruvallur_District_Tamil_Nadu-Vacations.html', u'/Tourism-g5074480-Mannargudi_Tamil_Nadu-Vacations.html', u'/Tourism-g1603630-Theni_Tamil_Nadu-Vacations.html', u'/Tourism-g641714-Madikeri_Kodagu_District_Karnataka-Vacations.html', u'/Tourism-g297586-Hyderabad_Telangana-Vacations.html', u'/Tourism-g304554-Mumbai_Bombay_Maharashtra-Vacations.html', u'/Tourism-g674818-Goverdhan_Uttar_Pradesh-Vacations.html', u'/Tourism-g1092107-McLeod_Ganj_Dharamsala_Himachal_Pradesh-Vacations.html', u'/Tourism-g635750-Shahpura_Rajasthan-Vacations.html', u'/Tourism-g1584823-Thiruvarur_Tamil_Nadu-Vacations.html', u'/Tourism-g2285288-Kuchaman_Rajasthan-Vacations.html', u'/Tourism-g2285982-Barpeta_Assam-Vacations.html', u'/Tourism-g1143166-Morni_Hills_Haryana-Vacations.html', u'/Tourism-g1379362-Masinagudi_Tamil_Nadu-Vacations.html', u'/Tourism-g1457276-Jamba_Rajasthan-Vacations.html', u'/Tourism-g3570382-Chandauli_Uttar_Pradesh-Vacations.html', u'/Tourism-g2287347-Daporijo_Arunachal_Pradesh-Vacations.html', u'/Tourism-g3736182-Draksharama_Andhra_Pradesh-Vacations.html', u'/Tourism-g5258996-Chithirapuram_Munnar_Kerala-Vacations.html', u'/Tourism-g2287538-Kamarpukur_West_Bengal-Vacations.html', u'/Tourism-g1162479-Kotagiri_Tamil_Nadu-Vacations.html', u'/Tourism-g1162349-Wellington_Tamil_Nadu-Vacations.html', u'/Tourism-g304555-Jaipur_Rajasthan-Vacations.html', u'/Tourism-g858473-Tinsukia_Assam-Vacations.html', u'/Tourism-g4310419-Kottakuppam_Tamil_Nadu-Vacations.html', u'/Tourism-g297683-Agra_Uttar_Pradesh-Vacations.html', u'/Tourism-g2282342-Tranquebar_Tamil_Nadu-Vacations.html', u'/Tourism-g1841213-Karur_Tamil_Nadu-Vacations.html', u'/Tourism-g1162294-Dhaulpur_Rajasthan-Vacations.html', u'/Tourism-g1490894-Basti_Uttar_Pradesh-Vacations.html', u'/Tourism-g1639623-Kutta_Kodagu_District_Karnataka-Vacations.html', u'/Tourism-g2282678-Lunglei_Mizoram-Vacations.html', u'/Tourism-g2289032-Tamenglong_Manipur-Vacations.html', u'/Tourism-g1162463-Samode_Rajasthan-Vacations.html', u'/Tourism-g3383679-Samalkha_Haryana-Vacations.html', u'/Tourism-g3566526-Tambaram_Tamil_Nadu-Vacations.html', u'/Tourism-g668045-Imphal_Manipur-Vacations.html', u'/Tourism-g858488-Kaziranga_National_Park_Assam-Vacations.html', u'/Tourism-g1891000-Anantnag_Kashmir_Jammu_and_Kashmir-Vacations.html', u'/Tourism-g1438747-Vizianagaram_Andhra_Pradesh-Vacations.html', u'/Tourism-g3746703-Kondapalle_Andhra_Pradesh-Vacations.html', u'/Tourism-g3903001-Gajraula_Uttar_Pradesh-Vacations.html', u'/Tourism-g1639501-Ammathi_Kodagu_District_Karnataka-Vacations.html', u'/Tourism-g2531476-Medchal_Andhra_Pradesh-Vacations.html', u'/Tourism-g858368-Saharanpur_Uttar_Pradesh-Vacations.html', u'/Tourism-g734453-Gorakhpur_Uttar_Pradesh-Vacations.html', u'/Tourism-g4025997-Nuzvid_Andhra_Pradesh-Vacations.html', u'/Tourism-g1047021-Sunauli_Uttar_Pradesh-Vacations.html', u'/Tourism-g2334910-Bhadohi_Uttar_Pradesh-Vacations.html', u'/Tourism-g2282879-Palani_Tamil_Nadu-Vacations.html', u'/Tourism-g297592-Patna_Bihar-Vacations.html', u'/Tourism-g297605-Candolim_Bardez_Goa-Vacations.html', u'/Tourism-g6771140-Azamgarh_Uttar_Pradesh-Vacations.html', u'/Tourism-g3948087-Amarnath_Yatra_Kashmir_Jammu_and_Kashmir-Vacations.html', u'/Tourism-g2242598-Jhajjar_Haryana-Vacations.html', u'/Tourism-g3997717-Ramnagar_Bihar-Vacations.html', u'/Tourism-g2282339-Tuensang_Nagaland-Vacations.html', u'/Tourism-g297589-Arunachal_Pradesh-Vacations.html', u'/Tourism-g1155937-Rajgir_Bihar-Vacations.html', u'/Tourism-g297676-Coonoor_Tamil_Nadu-Vacations.html', u'/Tourism-g1523688-Hudeel_Rajasthan-Vacations.html', u'/Tourism-g1162486-Velankanni_Tamil_Nadu-Vacations.html', u'/Tourism-g4444115-Bhadra_Rajasthan-Vacations.html', u'/Tourism-g2531326-Barabanki_Uttar_Pradesh-Vacations.html', u'/Tourism-g1154387-Manali_Tamil_Nadu-Vacations.html', u'/Tourism-g3592284-Mansarovar_Rajasthan-Vacations.html', u'/Tourism-g3385323-Kadmat_Lakshadweep-Vacations.html', u'/Tourism-g3581630-Parsoli_Rajasthan-Vacations.html', u'/Tourism-g2531531-Saiha_Mizoram-Vacations.html', u'/Tourism-g2305754-Srivilliputhur_Tamil_Nadu-Vacations.html', u'/Tourism-g5602899-Kolagappara_Wayanad_District_Kerala-Vacations.html', u'/Tourism-g679018-Alwar_Rajasthan-Vacations.html', u'/Tourism-g2531564-Gumla_Jharkhand-Vacations.html', u'/Tourism-g2732633-Kalapettai_Union_Territory_of_Pondicherry-Vacations.html', u'/Tourism-g2322205-Haflong_Assam-Vacations.html', u'/Tourism-g776433-Kushinagar_Uttar_Pradesh-Vacations.html', u'/Tourism-g2322083-Abhaneri_Rajasthan-Vacations.html', u'/Tourism-g3581769-Chalsa_West_Bengal-Vacations.html', u'/Tourism-g1007644-Pokaran_Rajasthan-Vacations.html', u'/Tourism-g2288629-Thirukkadaiyur_Tamil_Nadu-Vacations.html', u'/Tourism-g304551-New_Delhi_National_Capital_Territory_of_Delhi-Vacations.html', u'/Tourism-g2288597-Muzaffarpur_Bihar-Vacations.html', u'/Tourism-g3556333-Sathyamangalam_Tamil_Nadu-Vacations.html', u'/Tourism-g297615-Gurgaon_Haryana-Vacations.html', u'/Tourism-g297598-Silvassa_Dadra_and_Nagar_Haveli-Vacations.html', u'/Tourism-g2531560-Karimganj_Assam-Vacations.html', u'/Tourism-g7132598-Anpara_Uttar_Pradesh-Vacations.html', u'/Tourism-g1584814-Zirakpur_Chandigarh-Vacations.html', u'/Tourism-g4039725-Tiruchengode_Tamil_Nadu-Vacations.html', u'/Tourism-g970112-Osian_Rajasthan-Vacations.html', u'/Tourism-g2295143-Anantapur_Andhra_Pradesh-Vacations.html', u'/Tourism-g4013763-Gadwal_Telangana-Vacations.html', u'/Tourism-g1207704-Pilani_Rajasthan-Vacations.html', u'/Tourism-g4094067-Jaigaon_West_Bengal-Vacations.html', u'/Tourism-g1373035-Thiruchendur_Tamil_Nadu-Vacations.html', u'/Tourism-g7744184-Bilona_Rajasthan-Vacations.html', u'/Tourism-g1155135-Ranthambore_National_Park_Rajasthan-Vacations.html', u'/Tourism-g3931976-Murthal_Haryana-Vacations.html', u'/Tourism-g4013761-Dharmavaram_Andhra_Pradesh-Vacations.html', u'/Tourism-g2547320-Kannauj_Uttar_Pradesh-Vacations.html', u'/Tourism-g5978824-Meppadi_Wayanad_District_Kerala-Vacations.html', u'/Tourism-g297640-Lakshadweep-Vacations.html', u'/Tourism-g3248385-Turtuk_Nubra_Valley_Ladakh_Jammu_and_Kashmir-Vacations.html', u'/Tourism-g4300875-Elanthoppu_Tamil_Nadu-Vacations.html', u'/Tourism-g3383986-Sonepur_Bihar-Vacations.html', u'/Tourism-g797802-Fatehpur_Sikri_Uttar_Pradesh-Vacations.html', u'/Tourism-g677469-Faridabad_Haryana-Vacations.html', u'/Tourism-g6106256-Vazhavatta_Wayanad_District_Kerala-Vacations.html', u'/Tourism-g2516333-Falta_West_Bengal-Vacations.html', u'/Tourism-g3383708-Pehowa_Haryana-Vacations.html', u'/Tourism-g297675-Coimbatore_Tamil_Nadu-Vacations.html', u'/Tourism-g319729-Pushkar_Rajasthan-Vacations.html', u'/Tourism-g1152780-Vellore_Tamil_Nadu-Vacations.html', u'/Tourism-g1584851-Tirunelveli_Tamil_Nadu-Vacations.html', u'/Tourism-g1937007-Carmona_Salcette_District_Goa-Vacations.html', u'/Tourism-g2285507-Dispur_Assam-Vacations.html', u'/Tourism-g4036020-Tanuku_Andhra_Pradesh-Vacations.html', u'/Tourism-g1087540-Jagadhri_Haryana-Vacations.html', u'/Tourism-g1162447-Phalodi_Rajasthan-Vacations.html', u'/Tourism-g4044536-Patan_Rajasthan-Vacations.html', u'/Tourism-g1397068-Mahansar_Rajasthan-Vacations.html', u'/Tourism-g303894-Rameswaram_Tamil_Nadu-Vacations.html', u'/Tourism-g3317279-Yavakapadi_Village_Kodagu_District_Karnataka-Vacations.html', u'/Tourism-g1222238-Jind_Haryana-Vacations.html', u'/Tourism-g2042157-Nagaur_Rajasthan-Vacations.html', u'/Tourism-g1234703-Howrah_West_Bengal-Vacations.html', u'/Tourism-g1602164-Barmer_Rajasthan-Vacations.html', u'/Tourism-g1890809-Qadian_Gurdaspur_District_Punjab-Vacations.html', u'/Tourism-g503707-Kalimpong_West_Bengal-Vacations.html', u'/Tourism-g3387067-Amroha_Uttar_Pradesh-Vacations.html', u'/Tourism-g297666-Bikaner_Rajasthan-Vacations.html', u'/Tourism-g1024713-Kharagpur_West_Bengal-Vacations.html', u'/Tourism-g1985453-Srikalahasti_Andhra_Pradesh-Vacations.html', u'/Tourism-g6654287-Dwaraka_Tirumala_Andhra_Pradesh-Vacations.html', u'/Tourism-g1214902-Sangla_Kinnaur_District_Himachal_Pradesh-Vacations.html', u'/Tourism-g668044-Kohima_Nagaland-Vacations.html', u'/Tourism-g1584815-Kalpa_Kinnaur_District_Himachal_Pradesh-Vacations.html', u'/Tourism-g946396-Itanagar_Arunachal_Pradesh-Vacations.html', u'/Tourism-g2531516-Phek_Nagaland-Vacations.html', u'/Tourism-g608474-Lonavala_Maharashtra-Vacations.html', u'/Tourism-g1443432-Barli_Rajasthan-Vacations.html', u'/Tourism-g1486557-Kushalnagar_Kodagu_District_Karnataka-Vacations.html', u'/Tourism-g4468377-Sasan_Gir_Gir_National_Park_Gujarat-Vacations.html', u'/Tourism-g1639852-Manchalli_Kodagu_District_Karnataka-Vacations.html', u'/Tourism-g1139022-Hissar_Haryana-Vacations.html', u'/Tourism-g1638801-Somvarpet_Kodagu_District_Karnataka-Vacations.html', u'/Tourism-g1749691-Mettupalayam_Tamil_Nadu-Vacations.html', u'/Tourism-g3581633-Marchula_Jim_Corbett_National_Park_Uttarakhand-Vacations.html', u'/Tourism-g2011747-Nagore_Tamil_Nadu-Vacations.html', u'/Tourism-g4036019-Tandur_Telangana-Vacations.html', u'/Tourism-g1162476-Erode_Tamil_Nadu-Vacations.html', u'/Tourism-g1383209-Swamimalai_Tamil_Nadu-Vacations.html', u'/Tourism-g1591396-Tura_Meghalaya-Vacations.html', u'/Tourism-g2287421-Balurghat_West_Bengal-Vacations.html', u'/Tourism-g2288622-Bhadrachalam_Telangana-Vacations.html', u'/Tourism-g6413197-Melmaruvathur_Tamil_Nadu-Vacations.html', u'/Tourism-g503702-Shillong_Meghalaya-Vacations.html', u'/Tourism-g2282646-Pulicat_Tamil_Nadu-Vacations.html', u'/Tourism-g3592214-Manimajra_Chandigarh-Vacations.html', u'/Tourism-g4915195-Rampur_Uttar_Pradesh-Vacations.html', u'/Tourism-g608476-Kanyakumari_Tamil_Nadu-Vacations.html', u'/Tourism-g1026932-Karaikudi_Tamil_Nadu-Vacations.html', u'/Tourism-g2285338-Mangaldai_Assam-Vacations.html', u'/Tourism-g7198808-Rinchenpong_West_Sikkim_Sikkim-Vacations.html', u'/Tourism-g6939236-Pulpally_Wayanad_District_Kerala-Vacations.html', u'/Tourism-g1016340-Ghanerao_Rajasthan-Vacations.html', u'/Tourism-g1162444-Nathdwara_Rajasthan-Vacations.html', u'/Tourism-g858483-Tawang_Arunachal_Pradesh-Vacations.html', u'/Tourism-g3387082-Nawabganj_Uttar_Pradesh-Vacations.html', u'/Tourism-g2360183-Sitapur_Uttar_Pradesh-Vacations.html', u'/Tourism-g3581726-Charkhari_Uttar_Pradesh-Vacations.html', u'/Tourism-g951350-Vrindavan_Uttar_Pradesh-Vacations.html', u'/Tourism-g2561302-Bandikui_Rajasthan-Vacations.html', u'/Tourism-g3382376-Diglipur_North_Andaman_Island_Andaman_and_Nicobar_Islands-Vacations.html', u'/Tourism-g7195242-Dibiyapur_Uttar_Pradesh-Vacations.html', u'/Tourism-g3179401-Amalapuram_Andhra_Pradesh-Vacations.html', u'/Tourism-g1162491-Chail_Uttar_Pradesh-Vacations.html', u'/Tourism-g7698336-Barh_Bihar-Vacations.html', u'/Tourism-g2322181-Devgarh_Rajasthan-Vacations.html', u'/Tourism-g1162539-Raichak_West_Bengal-Vacations.html', u'/Tourism-g2289017-Along_Arunachal_Pradesh-Vacations.html', u'/Tourism-g297681-Tripura-Vacations.html', u'/Tourism-g1155926-Jorhat_Assam-Vacations.html', u'/Tourism-g1638443-Balotra_Rajasthan-Vacations.html', u'/Tourism-g6950297-Orai_Uttar_Pradesh-Vacations.html', u'/Tourism-g1638802-Virajpet_Kodagu_District_Karnataka-Vacations.html', u'/Tourism-g665916-Bera_Rajasthan-Vacations.html', u'/Tourism-g5978850-Kattikkulam_Wayanad_District_Kerala-Vacations.html', u'/Tourism-g1025488-Dibrugarh_Assam-Vacations.html', u'/Tourism-g1639504-Siddapura_Kodagu_District_Karnataka-Vacations.html', u'/Tourism-g3931971-Khurja_Uttar_Pradesh-Vacations.html', u'/Tourism-g3581782-Achrol_Rajasthan-Vacations.html', u'/Tourism-g3383981-Gonda_Uttar_Pradesh-Vacations.html', u'/Tourism-g1675583-Ambala_Haryana-Vacations.html', u'/Tourism-g297644-Kavaratti_Island_Lakshadweep-Vacations.html', u'/Tourism-g2289073-Sitamarhi_Bihar-Vacations.html', u'/Tourism-g3224191-Bhimavaram_Andhra_Pradesh-Vacations.html', u'/Tourism-g1453998-Faizabad_Uttar_Pradesh-Vacations.html', u'/Tourism-g2037918-Sibsagar_Assam-Vacations.html', u'/Tourism-g297602-National_Capital_Territory_of_Delhi-Vacations.html', u'/Tourism-g1890762-Batala_Gurdaspur_District_Punjab-Vacations.html', u'/Tourism-g6351733-Manalur_Tamil_Nadu-Vacations.html', u'/Tourism-g297685-Varanasi_Uttar_Pradesh-Vacations.html', u'/Tourism-g1436005-Bolpur_West_Bengal-Vacations.html', u'/Tourism-g2285515-Diphu_Assam-Vacations.html', u'/Tourism-g7032283-Perambalur_Tamil_Nadu-Vacations.html', u'/Tourism-g1397174-Jojawar_Rajasthan-Vacations.html', u'/Tourism-g6510681-Ramnagar_Jim_Corbett_National_Park_Uttarakhand-Vacations.html', u'/Tourism-g2531351-Daltenganj_Jharkhand-Vacations.html', u'/Tourism-g668046-Cherrapunjee_Meghalaya-Vacations.html', u'/Tourism-g3721797-Ambalavayal_Wayanad_District_Kerala-Vacations.html', u'/Tourism-g4055365-Kanipakam_Andhra_Pradesh-Vacations.html', u'/Tourism-g3581623-Raebareli_Uttar_Pradesh-Vacations.html', u'/Tourism-g2289007-Mudumalai_Tamil_Nadu-Vacations.html', u'/Tourism-g1597579-Kavali_Andhra_Pradesh-Vacations.html', u'/Tourism-g1421760-Bagdogra_West_Bengal-Vacations.html', u'/Tourism-g2285343-Mandarmani_West_Bengal-Vacations.html', u'/Tourism-g2531379-Dumka_Jharkhand-Vacations.html', u'/Tourism-g1651181-Tarapith_West_Bengal-Vacations.html', u'/Tourism-g1627620-Beawar_Rajasthan-Vacations.html', u'/Tourism-g3385294-Agatti_Lakshadweep-Vacations.html', u'/Tourism-g304556-Chennai_Madras_Tamil_Nadu-Vacations.html', u'/Tourism-g6550658-Vikarabad_Telangana-Vacations.html', u'/Tourism-g4036015-Ramachandrapuram_Andhra_Pradesh-Vacations.html', u'/Tourism-g3657342-Arakkonam_Tamil_Nadu-Vacations.html', u'/Tourism-g2294718-Valmiki_National_Park_Bihar-Vacations.html', u'/Tourism-g1639845-Kakkabe_Kodagu_District_Karnataka-Vacations.html', u'/Tourism-g2422960-Tajpur_Bihar-Vacations.html', u'/Tourism-g1510736-Alsisar_Rajasthan-Vacations.html', u'/Tourism-g304557-Darjeeling_West_Bengal-Vacations.html', u'/Tourism-g4341131-Chakzot_Hunder_Nubra_Valley_Ladakh_Jammu_and_Kashmir-Vacations.html', u'/Tourism-g4340716-Tajpur_West_Bengal-Vacations.html', u'/Tourism-g1062901-Ghaziabad_Uttar_Pradesh-Vacations.html', u'/Tourism-g7148304-Ballia_Uttar_Pradesh-Vacations.html', u'/Tourism-g2287529-Bankura_West_Bengal-Vacations.html', u'/Tourism-g5970556-Banda_Uttar_Pradesh-Vacations.html', u'/Tourism-g1219610-Amaravathi_Andhra_Pradesh-Vacations.html', u'/Tourism-g1162480-Mahabalipuram_Tamil_Nadu-Vacations.html', u'/Tourism-g2559924-Hoskeri_Village_Kodagu_District_Karnataka-Vacations.html', u'/Tourism-g4915162-Fatehabad_Haryana-Vacations.html', u'/Tourism-g297672-Udaipur_Rajasthan-Vacations.html', u'/Tourism-g2285992-Pudukkottai_Tamil_Nadu-Vacations.html', u'/Tourism-g2698258-Dhikuli_Jim_Corbett_National_Park_Uttarakhand-Vacations.html', u'/Tourism-g2334950-Palolem_Canacona_Goa-Vacations.html', u'/Tourism-g1162533-Digha_West_Bengal-Vacations.html', u'/Tourism-g2647335-Cherai_Beach_Vypin_Island_Kochi_Cochin_Kerala-Vacations.html', u'/Tourism-g2288617-Jamwa_Ramgarh_Rajasthan-Vacations.html', u'/Tourism-g2531554-Tarakeswar_West_Bengal-Vacations.html', u'/Tourism-g297622-Kashmir_Jammu_and_Kashmir-Vacations.html', u'/Tourism-g2322266-Pipraich_Uttar_Pradesh-Vacations.html', u'/Tourism-g297584-Port_Blair_South_Andaman_Island_Andaman_and_Nicobar_Islands-Vacations.html', u'/Tourism-g2282793-Manas_National_Park_Assam-Vacations.html', u'/Tourism-g5870391-Lalitpur_Uttar_Pradesh-Vacations.html', u'/Tourism-g1102838-Hosur_Tamil_Nadu-Vacations.html', u'/Tourism-g1028662-Agartala_Tripura-Vacations.html', u'/Tourism-g1239601-Patnem_Canacona_Goa-Vacations.html', u'/Tourism-g776956-Mahwah_Rajasthan-Vacations.html', u'/Tourism-g297624-Ladakh_Jammu_and_Kashmir-Vacations.html', u'/Tourism-g2322114-Aldona_Bardez_Goa-Vacations.html', u'/Tourism-g3841232-Wayanad_District_Kerala-Vacations.html', u'/Tourism-g7741550-Mayabunder_North_Andaman_Island_Andaman_and_Nicobar_Islands-Vacations.html', u'/Tourism-g2642525-Mailam_Tamil_Nadu-Vacations.html', u'/Tourism-g659786-Siliguri_West_Bengal-Vacations.html', u'/Tourism-g297668-Jodhpur_Rajasthan-Vacations.html', u'/Tourism-g5602904-Mathamangalam_Wayanad_District_Kerala-Vacations.html', u'/Tourism-g297591-Bihar-Vacations.html', u'/Tourism-g4354974-Sernabatim_Salcette_District_Goa-Vacations.html', u'/Tourism-g1238252-Fatehpur_Rajasthan-Vacations.html', u'/Tourism-g3680086-Kanathur_Tamil_Nadu-Vacations.html', u'/Tourism-g679029-Jhansi_Uttar_Pradesh-Vacations.html', u'/Tourism-g2531331-Barddhaman_West_Bengal-Vacations.html', u'/Tourism-g5869872-Begusarai_Bihar-Vacations.html', u'/Tourism-g616028-Haridwar_Uttarakhand-Vacations.html', u'/Tourism-g1156065-Bokaro_Jharkhand-Vacations.html', u'/Tourism-g297587-Tirupati_Andhra_Pradesh-Vacations.html', u'/Tourism-g2287352-Cuddalore_Tamil_Nadu-Vacations.html', u'/Tourism-g3746896-Dhanwar_Jharkhand-Vacations.html', u'/Tourism-g4760565-Edavanakkad_Vypin_Island_Kochi_Cochin_Kerala-Vacations.html', u'/Tourism-g304558-Kolkata_Calcutta_West_Bengal-Vacations.html', u'/Tourism-g2288628-Ongole_Andhra_Pradesh-Vacations.html', u'/Tourism-g297626-Jharkhand-Vacations.html', u'/Tourism-g1025163-Assagao_Bardez_Goa-Vacations.html', u'/Tourism-g503705-Kanchipuram_Tamil_Nadu-Vacations.html', u'/Tourism-g2287353-Covelong_Tamil_Nadu-Vacations.html', u'/Tourism-g303886-Bharatpur_Rajasthan-Vacations.html', u'/Tourism-g303887-Bundi_Rajasthan-Vacations.html', u'/Tourism-g297669-Kumbhalgarh_Rajasthan-Vacations.html', u'/Tourism-g7208256-Baghpat_Uttar_Pradesh-Vacations.html', u'/Tourism-g1943018-Mirik_West_Bengal-Vacations.html', u'/Tourism-g2289072-Sivakasi_Tamil_Nadu-Vacations.html', u'/Tourism-g2285408-Jhumri_telaiya_Jharkhand-Vacations.html', u'/Tourism-g297594-Chhattisgarh-Vacations.html', u'/Tourism-g1584828-Mandarmoni_West_Bengal-Vacations.html', u'/Tourism-g1584790-Birpara_West_Bengal-Vacations.html', u'/Tourism-g1156015-Hansi_Haryana-Vacations.html', u'/Tourism-g4093423-Kelambakkam_Tamil_Nadu-Vacations.html', u'/Tourism-g3386997-Bhitarkanika_National_Park_Kendrapara_Odisha-Vacations.html', u'/Tourism-g6279667-Palakollu_Andhra_Pradesh-Vacations.html', u'/Tourism-g4915215-Rajapalayam_Tamil_Nadu-Vacations.html', u'/Tourism-g6495768-Taoru_Haryana-Vacations.html', u'/Tourism-g2282385-Nongstoin_Meghalaya-Vacations.html', u'/Tourism-g1830829-Jammu_Jammu_and_Kashmir-Vacations.html', u'/Tourism-g970307-Kalka_Haryana-Vacations.html', u'/Tourism-g1005753-Khammam_Telangana-Vacations.html', u'/Tourism-g4053233-Nadia_West_Bengal-Vacations.html', u'/Tourism-g3976771-Virudhunagar_Tamil_Nadu-Vacations.html', u'/Tourism-g297616-Panchkula_Haryana-Vacations.html', u'/Tourism-g297657-Meghalaya-Vacations.html', u'/Tourism-g2278123-Pali_Rajasthan-Vacations.html', u'/Tourism-g3948102-Badrinath_Yatra_Uttarakhand-Vacations.html', u'/Tourism-g297633-Kochi_Cochin_Kerala-Vacations.html', u'/Tourism-g3386854-Kendrapara_Odisha-Vacations.html', u'/Tourism-g1890758-Gurdaspur_District_Punjab-Vacations.html', u'/Tourism-g1816362-Sriperumbudur_Tamil_Nadu-Vacations.html', u'/Tourism-g3320410-Malpura_Rajasthan-Vacations.html', u'/Tourism-g1162467-Sariska_Rajasthan-Vacations.html', u'/Tourism-g7296791-Sundarban_West_Bengal-Vacations.html', u'/Tourism-g1639858-Ponnampet_Kodagu_District_Karnataka-Vacations.html', u'/Tourism-g2531543-Singhpur_Uttar_Pradesh-Vacations.html', u'/Tourism-g2285322-Marigaon_Assam-Vacations.html', u'/Tourism-g3581775-Bijaynagar_Rajasthan-Vacations.html', u'/Tourism-g2322303-Sikar_Rajasthan-Vacations.html', u'/Tourism-g2288627-Lepakshi_Andhra_Pradesh-Vacations.html', u'/Tourism-g2068870-Srisailam_Andhra_Pradesh-Vacations.html', u'/Tourism-g790279-Kumbakonam_Tamil_Nadu-Vacations.html', u'/Tourism-g1432228-Midnapore_West_Bengal-Vacations.html', u'/Tourism-g7743219-Dakshin_Dhupjhora_West_Bengal-Vacations.html', u'/Tourism-g2265353-Taki_West_Bengal-Vacations.html', u'/Tourism-g1207709-Kurseong_West_Bengal-Vacations.html', u'/Tourism-g3538118-Kangri_Haridwar_Uttarakhand-Vacations.html', u'/Tourism-g1096234-Amer_Rajasthan-Vacations.html', u'/Tourism-g306996-Canacona_Goa-Vacations.html', u'/Tourism-g1162321-Jhunjhunu_Rajasthan-Vacations.html', u'/Tourism-g297671-Sawai_Madhopur_Rajasthan-Vacations.html', u'/Tourism-g2322251-Orang_Assam-Vacations.html', u'/Tourism-g4025951-Kandukur_Andhra_Pradesh-Vacations.html', u'/Tourism-g2285414-Jhalawar_Rajasthan-Vacations.html', u'/Tourism-g858482-Bomdila_Arunachal_Pradesh-Vacations.html', u'/Tourism-g1152790-Gorumara_National_Park_West_Bengal-Vacations.html', u'/Tourism-g297620-Jammu_City_Jammu_Jammu_and_Kashmir-Vacations.html', u'/Tourism-g303888-Chittaurgarh_Rajasthan-Vacations.html', u'/Tourism-g2295148-Sri_Ganganagar_Rajasthan-Vacations.html', u'/Tourism-g2295092-Bishnupur_West_Bengal-Vacations.html', u'/Tourism-g2185944-Sohna_Haryana-Vacations.html', u'/Tourism-g297590-Assam-Vacations.html', u'/Tourism-g2412280-Villupuram_Tamil_Nadu-Vacations.html', u'/Tourism-g608475-Kota_Rajasthan-Vacations.html', u'/Tourism-g2424471-Tala_Bandhavgarh_National_Park_Madhya_Pradesh-Vacations.html', u'/Tourism-g1584858-West_Sikkim_Sikkim-Vacations.html', u'/Tourism-g1156064-Udhampur_Jammu_Jammu_and_Kashmir-Vacations.html', u'/Tourism-g317097-Abu_Rajasthan-Vacations.html', u'/Tourism-g2732618-Dechu_Rajasthan-Vacations.html', u'/Tourism-g2282894-Adilabad_Telangana-Vacations.html', u'/Tourism-g735768-Warangal_Telangana-Vacations.html', u'/Tourism-g3445148-Barauni_Bihar-Vacations.html', u'/Tourism-g2285397-Jowai_Meghalaya-Vacations.html', u'/Tourism-g2294786-Lava_West_Bengal-Vacations.html', u'/Tourism-g2322321-Tiruchendur_Tamil_Nadu-Vacations.html', u'/Tourism-g2531423-Koch_Bihar_West_Bengal-Vacations.html', u'/Tourism-g2282674-Madhubani_Bihar-Vacations.html', u'/Tourism-g2531494-Neora_West_Bengal-Vacations.html', u'/Tourism-g679039-Bandhavgarh_National_Park_Madhya_Pradesh-Vacations.html', u'/Tourism-g1974063-Araku_Valley_Andhra_Pradesh-Vacations.html', u'/Tourism-g734456-Gaya_Bihar-Vacations.html', u'/Tourism-g3841234-Kenichira_Wayanad_District_Kerala-Vacations.html', u'/Tourism-g297585-Andhra_Pradesh-Vacations.html', u'/Tourism-g2645493-Shahjahanpur_Uttar_Pradesh-Vacations.html', u'/Tourism-g3384333-Mopidevi_Andhra_Pradesh-Vacations.html', u'/Tourism-g1973306-Nawada_Bihar-Vacations.html', u'/Tourism-g1408029-Kanadukathan_Tamil_Nadu-Vacations.html', u'/Tourism-g1156018-Pinjore_Haryana-Vacations.html', u'/Tourism-g858472-Silchar_Assam-Vacations.html', u'/Tourism-g679014-Secunderabad_Telangana-Vacations.html', u'/Tourism-g1156019-Thanesar_Haryana-Vacations.html', u'/Tourism-g2285457-Godda_Jharkhand-Vacations.html', u'/Tourism-g4153646-Lepchajagat_West_Bengal-Vacations.html', u'/Tourism-g297646-Madhya_Pradesh-Vacations.html', u'/Tourism-g783982-Rohet_Rajasthan-Vacations.html', u'/Tourism-g7692647-Cherala_Srimangala_Kodagu_District_Karnataka-Vacations.html', u'/Tourism-g3948109-Chardham_Yatra-Vacations.html', u'/Tourism-g1544623-Nalgonda_Andhra_Pradesh-Vacations.html', u'/Tourism-g6679032-Wakro_Arunachal_Pradesh-Vacations.html', u'/Tourism-g2295007-Hanumangarh_Rajasthan-Vacations.html', u'/Tourism-g1925961-Betalbatim_Salcette_District_Goa-Vacations.html', u'/Tourism-g1162327-Karauli_Rajasthan-Vacations.html', u'/Tourism-g3691172-North_Andaman_Island_Andaman_and_Nicobar_Islands-Vacations.html', u'/Tourism-g297597-Dadra_and_Nagar_Haveli-Vacations.html', u'/Tourism-g2278116-Bulandshahr_Uttar_Pradesh-Vacations.html', u'/Tourism-g1009352-Yercaud_Tamil_Nadu-Vacations.html', u'/Tourism-g6634969-Ninnimamidi_Andhra_Pradesh-Vacations.html', u'/Tourism-g2295002-Jaldapara_Wildlife_Sanctuary_West_Bengal-Vacations.html', u'/Tourism-g660182-Dwarka_Gujarat-Vacations.html', u'/Tourism-g2531550-Sivaganga_Tamil_Nadu-Vacations.html', u'/Tourism-g3581723-Colachel_Tamil_Nadu-Vacations.html', u'/Tourism-g2322278-Pomburpa_Bardez_Goa-Vacations.html', u'/Tourism-g5868158-Chirala_Andhra_Pradesh-Vacations.html', u'/Tourism-g2295096-Bhalukpong_Assam-Vacations.html', u'/Tourism-g4559666-Farakka_West_Bengal-Vacations.html', u'/Tourism-g303893-Muttukadu_Tamil_Nadu-Vacations.html', u'/Tourism-g776431-Krishnanagar_West_Bengal-Vacations.html', u'/Tourism-g662320-Ranchi_Jharkhand-Vacations.html', u'/Tourism-g1155906-Puttaparthi_Andhra_Pradesh-Vacations.html', u'/Tourism-g2294826-Kalakho_Rajasthan-Vacations.html', u'/Tourism-g1486543-Churu_Rajasthan-Vacations.html', u'/Tourism-g480252-Shekhawati_Rajasthan-Vacations.html', u'/Tourism-g3862494-Sultanpur_Uttar_Pradesh-Vacations.html', u'/Tourism-g2531521-Pilibhit_Uttar_Pradesh-Vacations.html', u'/Tourism-g1893705-Bastar_District_Chhattisgarh-Vacations.html', u'/Tourism-g2282684-Latehar_Jharkhand-Vacations.html', u'/Tourism-g2289074-Sirohi_Rajasthan-Vacations.html', u'/Tourism-g1162499-Siana_Uttar_Pradesh-Vacations.html', u'/Tourism-g4187547-Gobichettipalayam_Tamil_Nadu-Vacations.html', u'/Tourism-g2531472-Mamit_Mizoram-Vacations.html', u'/Tourism-g1162495-Firozabad_Uttar_Pradesh-Vacations.html', u'/Tourism-g1818882-Thadlaskein_Meghalaya-Vacations.html', u'/Tourism-g503692-Guwahati_Assam-Vacations.html', u'/Tourism-g1023973-Dindigul_Tamil_Nadu-Vacations.html', u'/Tourism-g2288625-Govardhan_Uttar_Pradesh-Vacations.html', u'/Tourism-g1162289-Bhilwara_Rajasthan-Vacations.html', u'/Tourism-g2287355-Courtallam_Tamil_Nadu-Vacations.html', u'/Tourism-g6208779-Arrah_Bihar-Vacations.html', u'/Tourism-g1162529-Asansol_West_Bengal-Vacations.html', u'/Tourism-g4036017-Tadepalligudem_Andhra_Pradesh-Vacations.html', u'/Tourism-g2288647-Krishnagiri_Tamil_Nadu-Vacations.html', u'/Tourism-g667801-Aizawl_Mizoram-Vacations.html', u'/Tourism-g2285300-Motihari_Bihar-Vacations.html', u'/Tourism-g3721800-Sahibabad_Uttar_Pradesh-Vacations.html', u'/Tourism-g2531452-Lohardaga_Jharkhand-Vacations.html', u'/Tourism-g2285989-Dausa_Rajasthan-Vacations.html', u'/Tourism-g4971762-Little_Andaman_South_Andaman_Island_Andaman_and_Nicobar_Islands-Vacations.html', u'/Tourism-g1439834-Sultan_Battery_Wayanad_District_Kerala-Vacations.html', u'/Tourism-g2289040-Simhachalam_Andhra_Pradesh-Vacations.html', u'/Tourism-g5887558-Katihar_Bihar-Vacations.html', u'/Tourism-g2655030-Loleygaon_West_Bengal-Vacations.html', u'/Tourism-g2048675-Pakur_Jharkhand-Vacations.html', u'/Tourism-g297596-Chandigarh-Vacations.html', u'/Tourism-g2285991-Kotputli_Rajasthan-Vacations.html', u'/Tourism-g1486497-Tippi_Arunachal_Pradesh-Vacations.html', u'/Tourism-g2288642-Dharmapuri_Tamil_Nadu-Vacations.html', u'/Tourism-g2282613-Nanguneri_Tamil_Nadu-Vacations.html', u'/Tourism-g5978833-Vellamunda_Wayanad_District_Kerala-Vacations.html', u'/Tourism-g2531492-Muzaffarnagar_Uttar_Pradesh-Vacations.html', u'/Tourism-g2287525-Murshidabad_West_Bengal-Vacations.html', u'/Tourism-g1457560-Nellore_Andhra_Pradesh-Vacations.html', u'/Tourism-g5870393-Tezu_Arunachal_Pradesh-Vacations.html', u'/Tourism-g2051704-Falakata_West_Bengal-Vacations.html', u'/Tourism-g1890805-Gurdaspur_Gurdaspur_District_Punjab-Vacations.html', u'/Tourism-g4915206-Bijnor_Uttar_Pradesh-Vacations.html', u'/Tourism-g3746708-Rohtas_Bihar-Vacations.html', u'/Tourism-g1918377-Sam_Rajasthan-Vacations.html', u'/Tourism-g2027392-Garjia_Jim_Corbett_National_Park_Uttarakhand-Vacations.html', u'/Tourism-g1745275-Bardhaman_West_Bengal-Vacations.html', u'/Tourism-g297643-Kalpeni_Lakshadweep-Vacations.html', u'/Tourism-g2288641-Thiruvannamalai_Tamil_Nadu-Vacations.html', u'/Tourism-g297621-Katra_Jammu_Jammu_and_Kashmir-Vacations.html', u'/Tourism-g3136744-Sahibganj_Jharkhand-Vacations.html', u'/Tourism-g776434-Vaishali_Bihar-Vacations.html', u'/Tourism-g1985445-Ayodhya_Uttar_Pradesh-Vacations.html', u'/Tourism-g1893708-Kondagaon_Bastar_District_Chhattisgarh-Vacations.html', u'/Tourism-g858487-Khonsa_Arunachal_Pradesh-Vacations.html', u'/Tourism-g1973313-Saharsa_Bihar-Vacations.html', u'/Tourism-g1584808-Panipat_Haryana-Vacations.html', u'/Tourism-g2266543-Chittoor_Andhra_Pradesh-Vacations.html', u'/Tourism-g3346867-Purnia_Bihar-Vacations.html', u'/Tourism-g1397113-Bagar_Rajasthan-Vacations.html', u'/Tourism-g1945483-Manesar_Haryana-Vacations.html', u'/Tourism-g1584849-Rewari_Haryana-Vacations.html', u'/Tourism-g2204498-Moira_Bardez_Goa-Vacations.html', u'/Tourism-g2295164-Roing_Arunachal_Pradesh-Vacations.html', u'/Tourism-g317098-Tiruchirappalli_Tamil_Nadu-Vacations.html', u'/Tourism-g2396914-Huzurnagar_Andhra_Pradesh-Vacations.html', u'/Tourism-g7753810-Hardoi_Uttar_Pradesh-Vacations.html', u'/Tourism-g644044-Durgapur_West_Bengal-Vacations.html', u'/Tourism-g1235469-Yamunanagar_Haryana-Vacations.html', u'/Tourism-g2282865-Sundarbans_National_Park_West_Bengal-Vacations.html', u'/Tourism-g2287390-Buxar_Bihar-Vacations.html', u'/Tourism-g297677-Madurai_Tamil_Nadu-Vacations.html', u'/Tourism-g667805-Kanpur_Uttar_Pradesh-Vacations.html', u'/Tourism-g2531464-Machilipatnam_Andhra_Pradesh-Vacations.html', u'/Tourism-g644043-Noida_Uttar_Pradesh-Vacations.html', u'/Tourism-g297679-Ooty_Tamil_Nadu-Vacations.html', u'/Tourism-g1214324-Kalyani_West_Bengal-Vacations.html', u'/Tourism-g6487175-Tiruttani_Tamil_Nadu-Vacations.html', u'/Tourism-g1087539-Sonipat_Haryana-Vacations.html', u'/Tourism-g3207691-Mahendragarh_Haryana-Vacations.html', u'/Tourism-g1154347-Pathankot_Gurdaspur_District_Punjab-Vacations.html', u'/Tourism-g1216533-Rohtak_Haryana-Vacations.html', u'/Tourism-g658409-Moradabad_Uttar_Pradesh-Vacations.html', u'/Tourism-g2288637-Lakkidi_Wayanad_District_Kerala-Vacations.html', u'/Tourism-g2288630-Mayiladuthurai_Tamil_Nadu-Vacations.html', u'/Tourism-g2282895-Nameri_National_Park_Assam-Vacations.html', u'/Tourism-g4106795-Periyakulam_Tamil_Nadu-Vacations.html', u'/Tourism-g800435-Jagdalpur_Bastar_District_Chhattisgarh-Vacations.html', u'/Tourism-g2053551-Deshnoke_Rajasthan-Vacations.html', u'/Tourism-g1156430-Khandala_Lonavala_Maharashtra-Vacations.html', u'/Tourism-g2295042-Giridih_Jharkhand-Vacations.html', u'/Tourism-g1584800-Aligarh_Uttar_Pradesh-Vacations.html', u'/Tourism-g1486505-Dirang_Arunachal_Pradesh-Vacations.html', u'/Tourism-g644042-Tirupur_Tamil_Nadu-Vacations.html', u'/Tourism-g2289005-Mananthavady_Wayanad_District_Kerala-Vacations.html', u'/Tourism-g2546088-Tiruvannamalai_Tamil_Nadu-Vacations.html', u'/Tourism-g306993-Bardez_Goa-Vacations.html', u'/Tourism-g503697-Kodagu_District_Karnataka-Vacations.html', u'/Tourism-g1219611-Hastinapur_Uttar_Pradesh-Vacations.html', u'/Tourism-g297684-Lucknow_Uttar_Pradesh-Vacations.html', u'/Tourism-g4881376-Guduvancheri_Tamil_Nadu-Vacations.html', u'/Tourism-g297673-Sikkim-Vacations.html', u'/Tourism-g2161631-Kadapa_Andhra_Pradesh-Vacations.html', u'/Tourism-g297660-Odisha-Vacations.html', u'/Tourism-g1584791-Kurukshetra_Haryana-Vacations.html', u'/Tourism-g4013759-Bodhan_Telangana-Vacations.html', u'/Tourism-g297611-Gir_National_Park_Gujarat-Vacations.html', u'/Tourism-g2267189-Jhadol_Rajasthan-Vacations.html', u'/Tourism-g4297670-Raghunathpura_Rajasthan-Vacations.html', u'/Tourism-g1238632-Nawalgarh_Rajasthan-Vacations.html', u'/Tourism-g1841212-Gudalur_Tamil_Nadu-Vacations.html', u'/Tourism-g2204495-Sangolda_Bardez_Goa-Vacations.html', u'/Tourism-g1639861-Pollibetta_Kodagu_District_Karnataka-Vacations.html', u'/Tourism-g2289069-Yingkiong_Arunachal_Pradesh-Vacations.html', u'/Tourism-g2140594-Greater_Noida_Uttar_Pradesh-Vacations.html', u'/Tourism-g1155904-Kurnool_Andhra_Pradesh-Vacations.html', u'/Tourism-g2288632-Thiruthani_Tamil_Nadu-Vacations.html', u'/Tourism-g6771231-Tirumalaisamudram_Tamil_Nadu-Vacations.html', u'/Tourism-g3736209-Canning_West_Bengal-Vacations.html', u'/Tourism-g1187926-Malda_West_Bengal-Vacations.html', u'/Tourism-g1985457-Tirumala_Andhra_Pradesh-Vacations.html', u'/Tourism-g3929053-Nalanda_Bihar-Vacations.html', u'/Tourism-g1639510-Srimangala_Kodagu_District_Karnataka-Vacations.html', u'/Tourism-g2088085-Bahadurgarh_Haryana-Vacations.html', u'/Tourism-g2531545-Siuri_West_Bengal-Vacations.html', u'/Tourism-g3179404-Raiganj_West_Bengal-Vacations.html', u'/Tourism-g4013745-Uppalapadu_Andhra_Pradesh-Vacations.html', u'/Tourism-g297606-Salcette_District_Goa-Vacations.html', u'/Tourism-g2322130-Bahraich_Uttar_Pradesh-Vacations.html', u'/Tourism-g5978685-Mahulia_Jharkhand-Vacations.html', u'/Tourism-g2732669-Diamond_Harbour_West_Bengal-Vacations.html', u'/Tourism-g2285520-Dholpur_Rajasthan-Vacations.html', u'/Tourism-g2052419-Khuri_Rajasthan-Vacations.html', u'/Tourism-g303881-Munnar_Kerala-Vacations.html', u'/Tourism-g1602177-Chandannagar_West_Bengal-Vacations.html', u'/Tourism-g4025969-Mandapeta_Andhra_Pradesh-Vacations.html', u'/Tourism-g2282376-Pasighat_Arunachal_Pradesh-Vacations.html', u'/Tourism-g2289065-Samsing_West_Bengal-Vacations.html', u'/Tourism-g2287401-Bongaigaon_Assam-Vacations.html', u'/Tourism-g1162469-Tonk_Rajasthan-Vacations.html', u'/Tourism-g4013758-Anakapalle_Andhra_Pradesh-Vacations.html', u'/Tourism-g3136738-Bapatla_Andhra_Pradesh-Vacations.html', u'/Tourism-g6033149-Meenagadi_Wayanad_District_Kerala-Vacations.html', u'/Tourism-g2285442-Hailakandi_Assam-Vacations.html', u'/Tourism-g2546103-Navalur_Tamil_Nadu-Vacations.html', u'/Tourism-g503704-Kishangarh_Rajasthan-Vacations.html', u'/Tourism-g303876-Vijayawada_Andhra_Pradesh-Vacations.html', u'/Tourism-g3383700-Dharuhera_Haryana-Vacations.html', u'/Tourism-g1440264-Balipara_Assam-Vacations.html', u'/Tourism-g2531405-Kailashahar_Tripura-Vacations.html', u'/Tourism-g6849730-Devala_Tamil_Nadu-Vacations.html', u'/Tourism-g1639508-Madapura_Kodagu_District_Karnataka-Vacations.html', u'/Tourism-g1974060-Mantralayam_Andhra_Pradesh-Vacations.html', u'/Tourism-g790280-Chidambaram_Tamil_Nadu-Vacations.html', u'/Tourism-g3780960-Kinnaur_District_Himachal_Pradesh-Vacations.html', u'/Tourism-g2285429-Jalor_Rajasthan-Vacations.html', u'/Tourism-g1154364-Khimsar_Rajasthan-Vacations.html', u'/Tourism-g297600-Daman_Daman_and_Diu-Vacations.html', u'/Tourism-g6599996-Sirkazhi_Tamil_Nadu-Vacations.html', u'/Tourism-g1162490-Bareilly_Uttar_Pradesh-Vacations.html', u'/Tourism-g1639841-Napoklu_Kodagu_District_Karnataka-Vacations.html', u'/Tourism-g2531386-Golaghat_Assam-Vacations.html', u'/Tourism-g1137805-Dudhwa_National_Park_Uttar_Pradesh-Vacations.html', u'/Tourism-g3955077-Palwal_Haryana-Vacations.html', u'/Tourism-g2195931-Namakkal_Tamil_Nadu-Vacations.html', u'/Tourism-g1022761-Auroville_Union_Territory_of_Pondicherry-Vacations.html', u'/Tourism-g297663-Punjab-Vacations.html', u'/Tourism-g1162281-Bali_Rajasthan-Vacations.html', u'/Tourism-g2322244-Neemrana_Rajasthan-Vacations.html', u'/Tourism-g1477768-Kolli_Hills_Tamil_Nadu-Vacations.html', u'/Tourism-g3136739-Saligao_Bardez_Goa-Vacations.html', u'/Tourism-g6734302-Dharapuram_Tamil_Nadu-Vacations.html', u'/Tourism-g2287427-Bokaro_Steel_City_Jharkhand-Vacations.html', u'/Tourism-g2531474-Markapur_Telangana-Vacations.html', u'/Tourism-g4013769-Thirukadaiyur_Tamil_Nadu-Vacations.html', u'/Tourism-g4302971-Melaghar_Tripura-Vacations.html', u'/Tourism-g1209424-Mukutmanipur_West_Bengal-Vacations.html', u'/Tourism-g297604-Goa-Vacations.html', u'/Tourism-g2531468-Mahbubnagar_Telangana-Vacations.html', u'/Tourism-g1676038-Hogenakkal_Tamil_Nadu-Vacations.html', u'/Tourism-g2282610-Narnaul_Haryana-Vacations.html', u'/Tourism-g1498931-Alipura_Uttar_Pradesh-Vacations.html', u'/Tourism-g1154366-Ramgarh_Rajasthan-Vacations.html', u'/Tourism-g1162208-Mokokchung_Nagaland-Vacations.html', u'/Tourism-g2282363-Pollachi_Tamil_Nadu-Vacations.html', u'/Tourism-g2578869-Ajabgarh_Rajasthan-Vacations.html', u'/Tourism-g297678-Nagapattinam_Tamil_Nadu-Vacations.html', u'/Tourism-g2295101-Nizamabad_Telangana-Vacations.html', u'/Tourism-g2322191-Etawah_Uttar_Pradesh-Vacations.html', u'/Tourism-g2287320-Hooghly_West_Bengal-Vacations.html', u'/Tourism-g1202865-Chitrakoot_Uttar_Pradesh-Vacations.html', u'/Tourism-g3419480-Rawatbhata_Rajasthan-Vacations.html', u'/Tourism-g734454-Balrampur_Uttar_Pradesh-Vacations.html', u'/Tourism-g3648986-Darbhanga_Bihar-Vacations.html', u'/Tourism-g3649126-Madhepura_Bihar-Vacations.html', u'/Tourism-g3334106-Jalore_Rajasthan-Vacations.html', u'/Tourism-g2288613-Bhuvanagiri_Telangana-Vacations.html', u'/Tourism-g1720832-Birpur_Bihar-Vacations.html', u'/Tourism-g1509133-Khichan_Rajasthan-Vacations.html', u'/Tourism-g659793-Karaikal_Union_Territory_of_Pondicherry-Vacations.html', u'/Tourism-g303890-Kodaikanal_Tamil_Nadu-Vacations.html', u'/Tourism-g2289066-Salasar_Rajasthan-Vacations.html', u'/Tourism-g2322197-Gosaba_West_Bengal-Vacations.html', u'/Tourism-g3690315-South_Andaman_Island_Andaman_and_Nicobar_Islands-Vacations.html', u'/Tourism-g6436957-Kovilpatti_Tamil_Nadu-Vacations.html', u'/Tourism-g858476-Digboi_Assam-Vacations.html', u'/Tourism-g3935134-Bhiwani_Haryana-Vacations.html', u'/Tourism-g297667-Jaisalmer_Rajasthan-Vacations.html', u'/Tourism-g2308547-Eluru_Telangana-Vacations.html', u'/Tourism-g858486-Namdapha_National_Park_Arunachal_Pradesh-Vacations.html', u'/Tourism-g3200193-Vypin_Island_Kochi_Cochin_Kerala-Vacations.html', u'/Tourism-g793693-Tuticorin_Tamil_Nadu-Vacations.html', u'/Tourism-g1627604-Bhiwadi_Rajasthan-Vacations.html', u'/Tourism-g2287519-Jamtara_Jharkhand-Vacations.html', u'/Tourism-g2639498-Maragodu_Kodagu_District_Karnataka-Vacations.html', u'/Tourism-g2195095-Nagercoil_Tamil_Nadu-Vacations.html', u'/Tourism-g2295129-Thiruchirapalli_Tamil_Nadu-Vacations.html', u'/Tourism-g1549826-Dayapur_Island_West_Bengal-Vacations.html', u'/Tourism-g297601-Diu_Daman_and_Diu-Vacations.html', u'/Tourism-g2295103-Karimnagar_Andhra_Pradesh-Vacations.html', u'/Tourism-g297658-Mizoram-Vacations.html', u'/Tourism-g1156049-Nubra_Valley_Ladakh_Jammu_and_Kashmir-Vacations.html', u'/Tourism-g7296787-Raxaul_Bihar-Vacations.html', u'/Tourism-g2531403-Hindupur_Andhra_Pradesh-Vacations.html', u'/Tourism-g2322306-Silghat_Assam-Vacations.html', u'/Tourism-g659792-Pondicherry_Union_Territory_of_Pondicherry-Vacations.html', u'/Tourism-g1162497-Mirzapur_Uttar_Pradesh-Vacations.html', u'/Tourism-g2282660-Munger_Bihar-Vacations.html', u'/Tourism-g306992-Anjuna_Bardez_Goa-Vacations.html', u'/Tourism-g1152719-Patnitop_Jammu_Jammu_and_Kashmir-Vacations.html', u'/Tourism-g1152696-Ropar_Haryana-Vacations.html', u'/Tourism-g3149947-Valparai_Tamil_Nadu-Vacations.html', u'/Tourism-g2288593-Bhagalpur_Bihar-Vacations.html', u'/Tourism-g2282864-Tenkasi_Tamil_Nadu-Vacations.html', u'/Tourism-g4472770-Chengalpattu_Tamil_Nadu-Vacations.html', u'/Tourism-g2287431-Bihar_Sharif_Bihar-Vacations.html', u'/Tourism-g4475274-Kalapet_Union_Territory_of_Pondicherry-Vacations.html', u'/Tourism-g2406619-Purulia_West_Bengal-Vacations.html', u'/Tourism-g3581621-Ranipet_Tamil_Nadu-Vacations.html', u'/Tourism-g2295084-Bakkhali_West_Bengal-Vacations.html', u'/Tourism-g2289022-Adoni_Andhra_Pradesh-Vacations.html', u'/Tourism-g1584820-Midnapur_West_Bengal-Vacations.html', u'/Tourism-g297599-Daman_and_Diu-Vacations.html', u'/Tourism-g3657797-Sagar_Island_West_Bengal-Vacations.html', u'/Tourism-g1119849-Tharangambadi_Tamil_Nadu-Vacations.html', u'/Tourism-g1162333-Mandawa_Rajasthan-Vacations.html', u'/Tourism-g679012-Mount_Abu_Rajasthan-Vacations.html', u'/Tourism-g2294980-Kolasib_Mizoram-Vacations.html', u'/Tourism-g3649129-Siwan_Bihar-Vacations.html', u'/Tourism-g1549815-Jalpaiguri_West_Bengal-Vacations.html', u'/Tourism-g1177884-Nagarjuna_Sagar_Telangana-Vacations.html', u'/Tourism-g1584805-Karnal_Haryana-Vacations.html', u'/Tourism-g5561649-Bhalukpong_Arunachal_Pradesh-Vacations.html', u'/Tourism-g1724403-Siolim_Bardez_Goa-Vacations.html', u'/Tourism-g6598410-Dubrajpur_West_Bengal-Vacations.html', u'/Tourism-g1239464-Hajipur_Bihar-Vacations.html', u'/Tourism-g1639591-Suntikoppa_Kodagu_District_Karnataka-Vacations.html', u'/Tourism-g303885-Bassi_Rajasthan-Vacations.html', u'/Tourism-g2289064-Seraikela_Jharkhand-Vacations.html', u'/Tourism-g2285985-Guntur_Andhra_Pradesh-Vacations.html', u'/Tourism-g735771-Santiniketan_West_Bengal-Vacations.html', u'/Tourism-g2282331-Ziro_Arunachal_Pradesh-Vacations.html', u'/Tourism-g1207699-Kokrajhar_Assam-Vacations.html', u'/Tourism-g2287426-Hazaribagh_Jharkhand-Vacations.html', u'/Tourism-g2288643-Yelagiri_Tamil_Nadu-Vacations.html', u'/Tourism-g1162345-Salem_Tamil_Nadu-Vacations.html', u'/Tourism-g2288602-Samastipur_Bihar-Vacations.html', u'/Tourism-g1893710-Deoghar_Jharkhand-Vacations.html', u'/Tourism-g1162449-Ranakpur_Rajasthan-Vacations.html', u'/Tourism-g1024712-Dhemaji_Assam-Vacations.html', u'/Tourism-g297583-Andaman_and_Nicobar_Islands-Vacations.html', u'/Tourism-g1152784-Jim_Corbett_National_Park_Uttarakhand-Vacations.html', u'/Tourism-g297662-Union_Territory_of_Pondicherry-Vacations.html', u'/Tourism-g777778-Gogunda_Rajasthan-Vacations.html', u'/Tourism-g2282801-Bhandarej_Rajasthan-Vacations.html', u'/Tourism-g2285450-Gorubathan_West_Bengal-Vacations.html', u'/Tourism-g1232778-Kalpetta_Wayanad_District_Kerala-Vacations.html', u'/Tourism-g3935125-Kesariya_Bihar-Vacations.html', u'/Tourism-g4163528-Cooch_Behar_West_Bengal-Vacations.html', u'/Tourism-g1011999-Dhanbad_Jharkhand-Vacations.html', u'/Tourism-g317096-Ajmer_Rajasthan-Vacations.html', u'/Tourism-g503703-Puri_Odisha-Vacations.html', u'/Tourism-g3383978-Unnao_Uttar_Pradesh-Vacations.html', u'/Tourism-g4915158-Sumerpur_Rajasthan-Vacations.html', u'/Tourism-g297588-Visakhapatnam_Andhra_Pradesh-Vacations.html', u'/Tourism-g1584832-Kakinada_Andhra_Pradesh-Vacations.html', u'/Tourism-g4578150-Abu_Road_Rajasthan-Vacations.html', u'/Tourism-g7726069-Forbesganj_Bihar-Vacations.html', u'/Tourism-g7221557-Chooralmala_Wayanad_District_Kerala-Vacations.html', u'/Tourism-g1162206-Dimapur_Nagaland-Vacations.html', u'/Tourism-g303891-Kovalam_Tamil_Nadu-Vacations.html', u'/Tourism-g2289019-Alipore_West_Bengal-Vacations.html', u'/Tourism-g679690-Narlai_Rajasthan-Vacations.html', u'/Tourism-g297688-Mathura_Uttar_Pradesh-Vacations.html', u'/Tourism-g2285474-Gajner_Rajasthan-Vacations.html', u'/Tourism-g2555901-Kookas_Rajasthan-Vacations.html', u'/Tourism-g3383704-Kaithal_Haryana-Vacations.html', u'/Tourism-g1091050-Badrinath_Uttarakhand-Vacations.html', u'/Tourism-g2287424-Chaibasa_Jharkhand-Vacations.html', u'/Tourism-g1162488-Allahabad_Uttar_Pradesh-Vacations.html', u'/Tourism-g2051708-Lataguri_West_Bengal-Vacations.html', u'/Tourism-g2531328-Baran_Rajasthan-Vacations.html', u'/Tourism-g2288635-Vaduvanchal_Wayanad_District_Kerala-Vacations.html', u'/Tourism-g2287534-Navadvipa_West_Bengal-Vacations.html', u'/Tourism-g2412429-Patratu_Jharkhand-Vacations.html', u'/Tourism-g1162286-Behror_Rajasthan-Vacations.html', u'/Tourism-g2282628-Ramanathapuram_Tamil_Nadu-Vacations.html', u'/Tourism-g297659-Nagaland-Vacations.html', u'/Tourism-g2322214-Kallakkurichi_Tamil_Nadu-Vacations.html', u'/Tourism-g858475-Goalpara_Assam-Vacations.html', u'/Tourism-g1234713-Shankarpur_West_Bengal-Vacations.html', u'/Tourism-g2282651-Nalbari_Assam-Vacations.html', u'/Tourism-g303895-Udagamandalam_Tamil_Nadu-Vacations.html', u'/Tourism-g5602902-Thirunelly_Wayanad_District_Kerala-Vacations.html', u'/Tourism-g424926-Thanjavur_Tamil_Nadu-Vacations.html', u'/Tourism-g297619-Jammu_and_Kashmir-Vacations.html', u'/Tourism-g2236445-Mogra_Rajasthan-Vacations.html', u'/Tourism-g1532344-Navi_Mumbai_Mumbai_Bombay_Maharashtra-Vacations.html', u'/Tourism-g1985450-Sasaram_Bihar-Vacations.html', u'/Tourism-g1154394-Garhmukteshwar_Uttar_Pradesh-Vacations.html', u'/Tourism-g5292838-Pawalgarh_Jim_Corbett_National_Park_Uttarakhand-Vacations.html', u'/Tourism-g319724-Dharamsala_Himachal_Pradesh-Vacations.html', u'/Tourism-g297656-Manipur-Vacations.html', u'/Tourism-g2282624-Ramdevra_Rajasthan-Vacations.html', u'/Tourism-g1162536-Haldia_West_Bengal-Vacations.html', u'/Tourism-g2717680-Kanger_Valley_National_Park_Bastar_District_Chhattisgarh-Vacations.html', u'/Tourism-g2295087-Baikunthpur_Bihar-Vacations.html', u'/Tourism-g1162496-Meerut_Uttar_Pradesh-Vacations.html'])
    for location in list(locationList)[100:101]:
        vocationPage(location)
#         break
#     reviewParser('http://www.tripadvisor.com.sg/Hotel_Review-g315887-d579449-Reviews-or210-Gleeson_s_Townhouse_and_Restaurant-Roscommon_County_Roscommon_Western_Ireland.html#REVIEWS')
#     reviewParser('http://www.tripadvisor.com.sg/Hotel_Review-g298564-d1547516-Reviews-or420-Hotel_Mume-Kyoto_Kyoto_Prefecture_Kinki.html#REVIEWS')
    
