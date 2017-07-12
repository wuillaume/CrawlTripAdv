'''
Created on Jan 31, 2015
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
from distutils.command.config import config
jobidList = []
 

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
    req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
    webpage = urllib2.urlopen(req)
    soup = BeautifulSoup(webpage.read())
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
        req = urllib2.Request(tUrl, headers={'User-Agent' : "Magic Browser"}) 
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
         
    
if __name__ == "__main__":
#     loadData('../data/players/playerDetail')
    getFromLocal()
#     getRawPage()
#     getSimilarityFromLocal()
    
    
#to get the detail information of teams
#     for team in teamNames:
#         filename = team.split('/')[-2]
#         print filename
#         f = open('../data/teams/'+filename,'w')
#         teamUrl =  playersPreUrl + team
#         soup = getSoupFromUrl(teamUrl)
#         teamDetailList = crawlForTeamDetail(soup)
#         for i in teamDetailList:
#             f.write(filename+'\t'+'\t'.join(i))
#             f.write('\n')
#         f.close()
   
#to get the roster of the teams
#      soup = getSoupFromUrl('http://www.basketball-reference.com/teams/')
#    crawlForTeamNames(soup)
     
#to get roster of the players
#     playerList = playerUrls()
#     playerInfoList = crawlForPlayerNames(playerList)#   
    
#     f = open('../data/players/playerInfo','w')
#     for i in playerInfoList:f
#         print i
#         f.write('\t'.join(i))
#         f.write('\n')
#         
#     f.close()
#     print len(playerInfoList)
#     urlList = ['http://www.basketball-reference.com/players/a/ackeral01.html']


#to get the detail information of players
#     f = open('../data/players/playerDetail','a')
#     infoList = getNameList('../data/players/playerInfo')
#     for i in infoList[4256:]:
#         time.sleep(0.8)
#         finalResultList =[]
#         url = playersPreUrl+str(i[1])
#         result = crawlForPlayerDetail(url)
#         finalResultList.append(i)
#         finalResultList += result
#         print finalResultList
#         f.write(str(finalResultList))
#         f.write('\n')
#     
#     f.close()
    
#     result = crawlForPlayerDetail(urlList)
#     print result
