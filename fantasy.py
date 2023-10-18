from functions import calculateScore, getAthleteTime, loadAthletes, assignDrafts
import pygsheets
import pandas as pd

printCell = [68, 2] #where we start printing (MAKE SURE TO CHANGE EACH TIME)
#tgtMeet = ["Troy v. Athens & Troy MS City Meet"]
tgtMeet = ["Oakland County HS XC Open Race", "Oakland County XC HS Championships"]

drafts = assignDrafts()
IDS = loadAthletes()

#authorization
serviceFile = ""
with open("json.txt", "r") as file:
    for line in file:
        serviceFile = line
gc = pygsheets.authorize(service_file = serviceFile)

sh = gc.open("FANTASY")

# df = pd.DataFrame()

# for key in drafts:
#     val = drafts[key]
#     df[key] = [" "] + val



# # wks.set_dataframe(df, (1, 1))

wks = sh[0]
for captain in drafts:
    df = pd.DataFrame()
    team = drafts[captain]
    lis = []
    lis2 = []
    ctr = 0
    for runner in team:
        time = getAthleteTime(AID = IDS[runner], targetMeet = tgtMeet)
        lis.append(time)
        if time is not None:
            ctr += 1
    for time in lis:
        lis2.append(calculateScore(time))
    totalScore = sum(lis2)
    df[str(captain)] = team + ["", ""]
    df["Times"] = lis + ["Average:", "Total:"]
    df["Score"] = lis2 + [totalScore / ctr, totalScore] 
    wks.set_dataframe(df, printCell)
    wks.cell(printCell).set_text_format("bold", True)
    printCell[1] += 3



#row, column
# print(wks.cell((2, 1)))
# print(wks.cell((1, 2)))
# if (wks.cell((1, 2)).value == ""):
#     print('hi')