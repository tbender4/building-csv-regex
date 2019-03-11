import csv
import re

def shortHand(matchedSite):
    #print(matchedSite.groups())
    #convert to shorthand
    directionRegex = re.compile(r'North|South|East|West')
    banRegex = re.compile(r'Road|Street|Blouevard|Lane|Park|Way|Avenue|\-| \- ')
    output = []
    for address in matchedSite.groups():
        if directionRegex.search(address) != None:
            output.append(address[0].lower())  #first letter of direction, lowercase
            continue
        elif banRegex.search(address) != None:
            continue
        output.append(address.lower())
    return ''.join(output)

def siteGeneratorFromSiteList(fullSiteList):
    internalTemplate = "alias {}=\"192.168.{}.168\"\n"  #shortenedname, port no.
    externalTemplate = "alias {}=\"{}\"\n"  #shortenedname, port no.
    fullOutput = ""
    for site in fullSiteList:
        fullOutput += internalTemplate.format(site[1], site[0])
    fullOutput += "\n\n"
    for site in fullSiteList:
        fullOutput += externalTemplate.format(site[1] + "_ext", site[2])
    return fullOutput
csvFile = open('example.csv', 'r')
csvList = ""
with open('example.csv') as csvFile:
    csvReader = csv.reader(csvFile, delimiter=',')
    csvList = list(csvReader)

#regex_testing
siteTypeRegex = [re.compile(r'(^\d+) (North|South|East|West)? (\d+)(th|st|nd)')]
#125 West 110th
#251 1st Street

siteTypeRegex.append(re.compile(r'(^\d+) (\w+) (Road|Street|Blouevard|Lane|Park|Way|Avenue)'))
#213 Bay Street(Jersey City)
#105 Chambers Street

siteTypeRegex.append(re.compile(r'(^\d+)(\-| \- )(\d+) (\w+)'))
#25 - 27 Mercer Street

#siteShortHandList = []
fullSiteList = []
for site in csvList:
    matchedSite = None
    for siteRegex in siteTypeRegex:
        matchedSite = siteRegex.search(site[1])
        if matchedSite != None:
            break
    fullSiteList.append([site[0], shortHand(matchedSite), site[2]])

output = siteGeneratorFromSiteList(fullSiteList)
bashProfile = open("bash_profile", "w+")
bashProfile.write(output)

print("bash_profile created. Run: cat bash_profile >> ~/.bash_profile && source ./bash_profile.")
