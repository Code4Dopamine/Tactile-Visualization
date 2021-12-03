import sqlite3
from time import sleep
from bhaptics import haptic_player

import csv, json, copy


# ===== Initialize bHaptic Player =====
# player = haptic_player.HapticPlayer()
# sleep(0.1)
# sleep(2)
# ======== END Initialize ========

# ======== START OF VARIABLE LIST ========

# ======== bHaptic control ========
maxIntensityValue = 0 # Set max number on "intensity" (from intensity list)
interval = 0.5  # Wait time | for sleep() command


# ======== csvFile Var ========
# csvFile = "example.csv"
# csvFile = "CSVData/earthquake2.csv"
csvFile = "CSVData/Manipulate.csv"


csvHeaderList = []  # Header File "Types" for Dictionary Keys
csvDict = {}  # Dictionary made from ".csv" file, with list grouped
csvDictOrig = {} # Deep Copy of csvDict w/ "Index" and "Integrity" as int List
csvDictSize = 0;

# ======== RUNTIME VAR ========
csvParseCounter = 0     # index # of .csv File (Parser)
dotPointList = []       # "Dictionary Type" Intensity Value to be sent to bHaptic (matches Mode, size = 5 or 20) e.g. [{"index": i, "intensity": 100} }]
dotIntensityList = []   # int List for iterating Intensity value
mode4IntensityList = [] # mode4 Intensity List (max = column (4))
dateList = []

pathPointList = []          # List of [], each containing "parsed" dotPointIntensity List
pathPointCoordinate = []    # Return {"x":#, "y":#}? from openCV2 data points?

tactSuitColumn = [
            [0, 4, 8, 12, 16],
            [1, 5, 9, 13, 17],
            [2, 6, 10, 14, 18],
            [3, 7, 11, 15, 19]
        ]
option = copy.deepcopy(tactSuitColumn)
for v in option:
    v.reverse()
# reverse so tactSuit index is "parsed" bottom-up as follows
    #  [[16, 12, 8, 4, 0],
    #  [17, 13, 9, 5, 1],
    #  [18, 14, 10, 6, 2],
    #  [19, 15, 11, 7, 3]]

# ================ END OF VARIABLE LIST ================

# Main Functions

def getDate():
    # selection = "date, iso_code, new_cases"
    conn = sqlite3.connect('covid-world.db')
    c = conn.cursor()

    selection = "date"
    countryIsoCode = "JPN"
    # loc = "United States"
    intList = []
    executeStr = f"""SELECT {selection} FROM "covid-world" WHERE "iso_code" LIKE '%{countryIsoCode}%' ORDER BY "date" """

    for i, row in enumerate(c.execute(executeStr)):
        intList.append(row[0])
        # print(row)
    global dateList
    dateList = intList

    conn.close()


def getCSVData(file):
    result = {}
    headerList = []
    with open(file, encoding="utf-8-sig") as csvfile:
    # with open(file) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")

        for row in reader:
            for column, value in row.items():
                result.setdefault(column, []).append(value)

        for key in result.keys():
            headerList.append(key)


    global csvDict, csvHeaderList, csvDictSize
    csvDict = result  # update result to csvDict
    print(f'csvDictColumn =: {csvDict.keys()}| Type: {type(csvDict.keys())}')
    csvHeaderList = headerList  # create "Header" list on csvDict[Key]
    print(f'csvHeaderList: {csvHeaderList}| Type: {type(csvHeaderList)}')
    # print(f"DateList = {csvDict['Date']}")
    # csvDictSize = len(csvDict[1][0])

    # find Max Value to be divided by 100 (for intensity)
    # for value in

def addDotPoints(index, intensity):
    if (len(dotPointList) >= 4):
        dotPointList.pop(0)

    # json.dumps()
    dotPointList.append({'index': index, 'intensity': intensity})
    print(dotPointList)
    print("Length = ", len(dotPointList))

def submitDot(pointList):
    global durationMillis, interval, player
    if not isinstance(pointList,list):
        print("Error: SubmitDot List is not a iterable list")

    player.submit_dot("backFrame", "VestBack", pointList, durationMillis)
    sleep(interval)

def headerValueToInteger(headerName):
    # TODO: Perform check on 'csvDict[headerName]' to see list can be parsed to "int"?
    if isinstance(headerName,str):
        if headerName in csvDict:
            print('---- Coverting "',headerName, '" list into "int" List ---')
            intList = []
            for value in csvDict[headerName]:
                intList.append(int(value))

            uploadDict = {headerName: intList}
            csvDict.update(uploadDict)
            print
        else:
            print('Error: No "',headerName, '" found in Header')
    else:
        print('headerValueToInteger NOT StringValue')
    # print("intList =", intList, " type = ", type(intList[0]))


    # print("New Result Dict = ", csvDict)
    #
    # print("Date List = ", csvDict["date"])
    # print(csvDict["date"][0])
    # print("Date Type = ", type(csvDict["date"][0]))
    # print("Size:", len(csvDict["index"]))

def fixIndexKey():
    global csvDict, csvHeaderList
    newDict = {"index":csvDict[csvHeaderList[0]]}
    # print("OldKeys = ", csvDict.keys())
    # print("KeysType = ", type(csvDict.keys()))
    newList = list(csvDict.keys())

    # print("fixIndexKey", csvHeaderList[0])
    # print("fixIndexKey - Type =", type(csvHeaderList[0]))

    csvDict.pop(newList[0])
    csvDict.update(newDict)
    # print("UpdatedCSV =", csvDict["index"])
    # print("NewKeys of csvDict = ", csvDict.keys())

    newHeaderList = []
    for key in csvDict.keys():
        newHeaderList.append(key)

    # global csvHeaderList
    csvHeaderList = newHeaderList
    # print("New csvHeaderList =", csvHeaderList)
    # csvDict.pop[str(csvHeaderList[0])]
    # csvDict.update(newDict)

def intensityToInteger(intensityKey):
    global maxIntensityValue, csvDict, csvHeaderList

    if ("intensity") not in csvDict:
            print(f'Key "Intensity" not found, parsing {intensityKey} to generate "Intensity" List')

    intList = []
    for value in csvDict[intensityKey]:
        if int(value) > maxIntensityValue:
            maxIntensityValue = int(value)
        intList.append(int(value))
    uploadDict = {"intensity": intList}
    csvDict.update(uploadDict)
    print("---- Set MaxIntensityValue =", maxIntensityValue)



    # if ("intensity") not in csvDict:
    #     # d = {"intensity": [0,1,2,3]}
    #     # csvDict.update(d)
    #     csvHeaderList.append("intensity")
    #     print("Added Intensity Key + Value into csvDict")
    #     print('csvDict["intensity"] =', csvDict["intensity"])
    #     print("CSVHeader:", csvHeaderList)
    #
    #     intList = []
    #     for value in csvDict[intensityKey]:
    #         if int(value) > maxIntensityValue:
    #             maxIntensityValue = int(value)
    #         intList.append(int(value))
    #
    #     uploadDict = {"intensity": intList}
    #     csvDict.update(uploadDict)
    #     print("---- Set MaxIntensityValue =", maxIntensityValue)

    # elif isinstance(intensityKey,str) and "intensity" in csvDict:
    #     if intensityKey in csvDict:
    #         # print('Coverting "',intensityKey, '" list into "intensity" List')
    #         intList = []
    #         for value in csvDict[intensityKey]:
    #             if int(value) > maxIntensityValue:
    #                 maxIntensityValue = int(value)
    #             intList.append(int(value))
    #
    #         uploadDict = {intensityKey: intList}
    #         csvDict.update(uploadDict)
    #         print("---- Set MaxIntensityValue =", maxIntensityValue)
    #     else:
    #         print('Error: No "',intensityKey, '" intensity str found as csvDict["key"]')
    # else:
    #     print('headerValueToInteger NOT type STR')

def getMode4Level(value): # Returns 0-4 based on level for ""
    # table = [20,40,60,80,100]
    table = [0,20,40,60,80]
    for i, option in enumerate(table):
        # print(value, " > ", i)
        if value >= 101:
            print("=== ERROR: getMode4Level comparing issue")
        if value > option:
            # print("#",i)
            pass
        else:
            return i

def mode4():
    global mode4IntensityList, csvParseCounter, dotPointList, option

    # Add new Intensity Value based on Counter
    mode4IntensityList.append(dotIntensityList[csvParseCounter])
    if len(mode4IntensityList) > 4:
        # print("==== Popped Value:", mode4IntensityList[0], " ====")
        mode4IntensityList.pop(0)

    # Perform update based on mode4IntensityList value to tactSuit
    # output 'newlist' as dotPointList dictionary
    newlist = []

    # TODO: Could Implement Variation Change (swap "n" to read "list")
    """
        Requires:
        1. Generate "Difference List" (val = abs(val[index-1] - val[index])
        2. Parse "intensityVariation" List (generated = Max-1 Size)
        3. getMode4Level Comparator
    """
    for index, intensityValue in enumerate(mode4IntensityList):
        # intensityValue = mode4IntensityList[index]
        for n, tactIndex in enumerate(option[index]):
            # n for level comparison, min 0, max 4 (total:5)
            # print("index=",tactIndex, end = " ")
            if n <= getMode4Level(intensityValue):
                d = {"index": tactIndex, "intensity": intensityValue}
                # print("== added",d)
                newlist.append(d)
            else:
                d = {"index": tactIndex, "intensity": 0}
                # print("== 0 added", d)
                newlist.append(d)
    dotPointList = []
    dotPointList = newlist

# def updateDotPointList(csvList, maxValue, mode):
def updateDotPointList(mode):
    global dotPointList, csvParseCounter,csvDict,csvHeaderList

    # 20 = Per Dot, 5 = Vertical Display
    if mode == 20:
        d = {"index": csvParseCounter, "intensity": dotIntensityList[csvParseCounter]}
        dotPointList.append(d)
        if len(dotPointList) > mode:
            dotPointList.pop(0)
            # print("===== prev. size:",len(dotPointList), "| item popped:",dotPointList.pop(0), "| size now = ", len(dotPointList), "=====")
        for i, value in enumerate(dotPointList): #Re-Index List for HapticSuit
            dotPointList[i]["index"] = i

        # print("dotPointList =", dotPointList)

    elif mode == 4:
        mode4()

    elif mode == 1:
        pass
        # TODO: Single Point Manipulation


    else:
        print("Error: Unknown Mode Value")

def updatePathPointList(mode):
    global csvParseCounter, dotPointList
    if mode == 20:
        if len(dotPointList) > mode:
            print("===== prev. size:",len(dotPointList), "| item popped:",dotPointList.pop(0), "| size now = ", len(dotPointList), "=====")
        for i, value in enumerate(dotPointList): #Re-Index List for HapticSuit
            dotPointList[i]["index"] = i
    # submitPath(key, VestFront, [{x: 0.5, y: 0.5, intensity: 100,{x: 0, y: 0, intensity: 100,{x: 1, y: 0, intensity: 100], 1000)
    pass

def generateDotIntensityList(csvList, maxValue):
    global dotIntensityList
    for i in csvList:
        value = round(i * 100 / maxValue)
        dotIntensityList.append(value)


def main():
    """
    print("register CenterX")
    player.register("CenterX", "SpeedTest_1Sec.tact")
    print("register Circle")
    player.register("Circle", "SpeedTest_5Sec.tact")
    sleep(0.3)
    """

    # === Final Code ====
    # intensityToInteger("new_cases")
    # print("Type index", type(csvDict["index"][0]))
    # print("Type new_cases", type(csvDict["new_cases"][0]))

# =============== START STUFF ====================
    print("====== CSV File:", csvFile, "======")

    getCSVData(csvFile)  # Initialize Dict:"csvDict" & List:"csvHeaderList"
    fixIndexKey()  # Issue 1st Header issue in  Excel .csv?
    headerValueToInteger("index")  # set csvDict["index"] type str --> int
    print(f'csvHeaderList: {csvHeaderList}')

    intensityStr = "new_cases"  # set "Str" variable as intensity
    intensityToInteger(intensityStr)  # set csvDict["intensity"] type str --> int
    generateDotIntensityList(csvDict["intensity"], maxIntensityValue)  # Generate list based on Max value

    global csvDictOrig
    csvDictOrig = copy.deepcopy(csvDict)  # DeepCopy: For debugging purposes

    print("Type index =", type(csvDict["index"]), ", Length = ", len(csvDict["index"]))
    print("Type new_cases =", type(csvDict["intensity"][0]))
    print('csvDict["intensity"][size=', len(csvDict["intensity"]), "] = ", csvDict["intensity"])
    print("Intensity List 4th Value =", csvDict["intensity"][3])

    print("DotPointList =", dotPointList)

    # print("updateDotIntensityList[", len(dotIntensityList), "] = ", dotIntensityList)
    print(f'dotIntensityList[{len(dotIntensityList)}]={dotIntensityList}')
    csvDictSize = len(csvDict["intensity"])
    # print("List Length (counter) =", csvDictSize)
    print("csvDictSize (counter) =", csvDictSize)

# =============== END START STUFF ====================

# =============== Initialize Haptic Player ===============
    player = haptic_player.HapticPlayer()
    sleep(0.1)
    sleep(2)
    print("========= Haptic Player Activated ==========")
    wait = 0.22
    mode = 4  # 20 or 4
    millis = 220

    global csvParseCounter
    csvParseCounter = 150
# =============== End Initialize ===============

    pathPoint = [{"x": 0.5, "y": 0.5, "intensity": 100}]
    getDate()

    for i in range(5):
        # player.submit_dot("backFrame", "VestBack", [{"index": 1, "intensity": 100}, {"index": 4, "intensity": 100}, {"index": 8, "intensity": 100}], millis)
        player.submit_path("backFrame", "VestBack", pathPoint, millis)
        sleep(0.3)

    while csvParseCounter < csvDictSize-1:

        # updateDotPointList(csvDict["intensity"], maxIntensityValue, mode)
        updateDotPointList(mode)
        # print("Counter =", csvParseCounter)
        # print(f'#{csvParseCounter} | Date = {dateList[csvParseCounter-1]} | Cases = {csvDict["intensity"][csvParseCounter-1]}')
        print(f'#{csvParseCounter} | Date = {dateList[csvParseCounter]} | Cases = {csvDict["intensity"][csvParseCounter]}')

        # dotPointList.reverse()
        # TODO: Dictionary Value Reverse
        player.submit_dot("backFrame", "VestBack", dotPointList, millis)
        # print(f'DotPointList = {dotPointList}')
        sleep(wait)

        csvParseCounter += 1

    # print("csvDict = ", csvDict, "\n")

    # print("HeaderList =", csvHeaderList)
    # print("Type of file = ", type(csvHeaderList[0]))
    # print(csvDict[csvHeaderList[0]])
    # print(csvDict[csvHeaderList[0]][1])
    #
    # print("Size =", len(csvDict[csvHeaderList[0]]))

    # print("Type = ", csvDict["index"], )


    # while (csvCounter != csvDictSize):
    #     pass

# ================ THREADING TEST =================
    # from threading import Thread
    # from playsound import playsound
    #
    # def play_sound():
    #     playsound('welcome.mp3')
    #
    # thread = Thread(target=play_sound)
    # thread.start()
if __name__ == '__main__':
    main()



