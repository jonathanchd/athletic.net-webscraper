import requests
from bs4 import BeautifulSoup
import html5lib

def calculateScore(time):
    if time is None:
        return 0
    if isinstance(time, str):
        time = convertTime(time)
    maxTime = 25 #minutes
    maxTime *= 60 #convert to seconds
    return maxTime - time
    
#convert something like 19:00.5 to 1140.5 sec
def convertTime(time):
    if time is None:
        return None
    spt = time.split(":")
    ret = float(spt[0]) * 60.0
    spt2 = spt[1].split(".")
    ret += float(spt2[0]) + (0.1 * float(spt2[1]))
    return ret

#return None if no times, otherwise return the string representation
def getAthleteTime(AID, targetMeet, season = 2022, targetDis = "5,000 Meters", teamID = 12572):
    season = "season_" + str(season) + "4" + str(teamID)
    URL = "https://www.athletic.net/CrossCountry/Athlete.aspx?AID=" + str(AID)
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, "html5lib")
    table = soup.find("div", attrs = {"class" : "col-md-7 pull-md-5 col-xl-8 pull-xl-4 col-print-7 athleteResults"})
    if table is None:
        return None
    table = table.find("div", attrs = {"uib-collapse" : season})
    if table is None:
        return None
    results = table.find_all("table", attrs = {"class" : "table table-sm table-responsive table-hover"})
    races = table.find_all("h5")
    index = None #use results[index]
    for i in range(len(races)):
        if races[i].text == targetDis:
            index = i
            break
    if index is None:
        return None

    search = results[index]
    meets = []
    for meet in search.find_all("a"):
        if "meet" in meet["href"] or "result" in meet["href"]:
            meets.append(meet.text)
    temp = []
    for i in range(len(meets)):
        if i % 2 == 0:
            continue
        for val in targetMeet:
            if (meets[i] == val):
                return meets[i - 1].strip("SR")

#return a dict of {name : athlete ID}
def loadAthletes(filename = "aIDs.txt", skiplines = 1):
    ret = dict()
    with open(filename, "r") as file:
        for row in file.readlines()[skiplines:]:
            row = row.strip("\n").split(" ")
            ret[row[0]] = row[1]
    return ret

#retrun dict of {person : list of drafts}
def assignDrafts(filename = "drafts.txt", skiplines = 2):
    ret = dict()
    with open(filename, "r") as file:
        read = file.readlines()[skiplines:]
        currPerson = None
        for i in range(len(read)):
            row = read[i].strip("\n")
            if (row == ""):
                continue
            spt = row.split(" ")
            if len(spt) == 2: #new person
                currPerson = spt[0]
                ret[currPerson] = list()
            else:
                ret[currPerson].append(spt[0])
    return ret