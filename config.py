'''

@author: Wuil
'''
import re
playersPreUrl = 'http://www.basketball-reference.com/'
preUrl = 'http://www.tripadvisor.com.sg/'

teamNames = ['/teams/ATL/', '/teams/BOS/', '/teams/NJN/', '/teams/CHA/', '/teams/CHI/', \
             '/teams/CLE/', '/teams/DAL/', '/teams/DEN/', '/teams/DET/', '/teams/GSW/', \
             '/teams/HOU/', '/teams/IND/', '/teams/LAC/', '/teams/LAL/', '/teams/MEM/', \
             '/teams/MIA/', '/teams/MIL/', '/teams/MIN/', '/teams/NOH/', '/teams/NYK/', \
             '/teams/OKC/', '/teams/ORL/', '/teams/PHI/', '/teams/PHO/', '/teams/POR/', \
             '/teams/SAC/', '/teams/SAS/', '/teams/TOR/', '/teams/UTA/', '/teams/WAS/' ]

draftPattern = r'(?<=<br><span class="bold_text">Draft:</span>).*(?=<br>)'
draftPattern2 = r'(?<=</a>,)[^<]*'
draftPattern3 = r'(?<=/draft/)[^\.]*'
# *draftPattern = r"(?<=br).*" 

def getDraftInfo(inputStr):
    draftInfo = ''
    return draftInfo

if __name__ == "__main__":
    rinput = '<br><span class="bold_text">Draft:</span> <a href="/teams/DET/draft.html">Detroit Pistons</a>, 2nd round (30th pick, 60th overall), <a href="/draft/NBA_2005.html">2005 NBA Draft</a><br><span class="bold_text">NBA Debut:</span> <a '
    prog = re.compile(draftPattern)
    temp = prog.findall(rinput)[0]
    print temp
    
    print re.compile(draftPattern2).findall(temp)[0].strip()[:-1]
    
    print re.compile(draftPattern3).findall(temp)[0]
    
    
    
    
    
