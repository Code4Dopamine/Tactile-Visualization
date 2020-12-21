# =================================================================================
import cv2
import numpy as np
import sqlite3
from bhaptics import haptic_player
from time import sleep

pathPointList = []
countryPathPointCoordDic = {}       # For use in PathPoint (bHaptic Json)
# Example Output: {'USA': [156, 552], 'ZAF': [340, 301], 'JPN': [167, 71]}
coord_Dic = {}
# tempList = [("USA", 160, 539), ("JPN", 185, 306), ("BRA", 315, 260)]
countryList = ["USA", "ZAF", "JPN"]
sampleData = ['USA', '2020-01-23', '0']
maxCountryCases = {}  # USA, JPN, ZAF

# imageSize = [480, 699] #world2.jpg
imageSize = [550, 800] #world3.jpg
imageDir = "CSVData/world3.jpg"
imageDir_CV = "CSVData/world3+haptic.jpg"
imageDir_CV = "CSVData/world3+haptic.jpg"

# ======= Main Data & Parameters =======
CoVID_Data = {}
selection = "date, iso_code, new_cases"
debugSkip = 300   #0 = Normal Run,

wait = 0.2          #Determine Sleep time after haptic (match "millis" for no delay)
millis = 200        #Length of Vibration per "submit_path" to BHaptic Player

# Testing Only
dateList = []
intensityList = {"USA": [], "ZAF": [], "JPN": []}

displayText = ""



def initializeCovidWorldData():
    # ('USA', '2020-01-23', '0')
    conn = sqlite3.connect('covid-world.db')
    c = conn.cursor()

    # Get
    def getMaxCountryCases(countryIsoCode):
        str = f"""SELECT MAX(new_cases) FROM "covid-world" WHERE "iso_code" LIKE '%{countryIsoCode}%'"""
        c.execute(str)
        num = c.fetchone()
        # print(f'num={num} | type={type(num)}')
        return int(num[0])

    def generateCoVIDData(countryIsoCode):
        selection = "date, iso_code, new_cases"
        # loc = "United States"
        intList = []
        executeStr = f"""SELECT {selection} FROM "covid-world" WHERE "iso_code" LIKE '%{countryIsoCode}%' ORDER BY "date" """

        for i, row in enumerate(c.execute(executeStr)):
            if row[0] not in CoVID_Data.keys():  # List is empty
                dateList.append(row[0])
                d = {row[0]: {row[1]: int(row[2])}}
                CoVID_Data.update(d)
                # Below to generate intensity List, Not required
                intensityList[countryIsoCode].append(int(row[2]))

            else:
                d = {row[1]: int(row[2])}
                # print(d)
                CoVID_Data[row[0]].update(d)
                intensityList[countryIsoCode].append(int(row[2]))

    for countryISO in countryList:
        d = {countryISO: getMaxCountryCases(countryISO)}
        maxCountryCases.update(d)
        generateCoVIDData(countryISO)  # '2020-01-24': {'USA': 1, 'JPN': 0, 'ZAF': 0}

    # print("MaxCountryCases=", maxCountryCases)

    # selection = "date, iso_code, new_cases"
    # loc = "United States"
    #
    # executeStr = f"""SELECT {selection} FROM "covid-world" WHERE "iso_code" LIKE '%{loc}%' ORDER BY "date" """
    #
    # executeStr = r"""SELECT date, iso_code, new_cases FROM "main"."covid-world" WHERE "iso_code" LIKE '%JPN%'"""
    #
    # print(str(executeStr))
    # c.execute(executeStr)
    # # print(f'TotalRow = {len(c.fetchall())}')
    #
    # row = c.fetchone()
    # print("ROW=", row, "| Size =", len(row))
    #
    # for i in row:
    #     print(i)
    # print(type(row))

    # ('USA', '2020-01-23', '0')
    # selection = "date, iso_code, new_cases"

    # for i, row in enumerate(c.execute(executeStr)):
    #     infoDic = {"iso_code": row[1], "new_cases": row[2]}
    #     dateDic = {row[0]:infoDic}
    #     finalDic = {i}
    #     d = {i:row[1]: row[0], "date": row[0], "iso_code": row[0]}
    #     d2 = {}
    #     print(row)

    conn.close()


def addCountryXY_hapticSuit(name, x, y):
    newX = round(x / imageSize[0], 3)   # Round to 3 Decimals
    newY = round(y / imageSize[1], 3)

    d = {str(name): [newX, newY]}
    # print(f'{d} -- Type:{type(d)}')
    countryPathPointCoordDic.update(d)

def addCountryXY(name, x, y):
    d = {str(name): [x, y]}
    # print(f'{d} -- Type:{type(d)}')
    coord_Dic.update(d)

def runCV2():
    # TODO: Add "mode" argument for image switch when performing test? (imageDir_CV)

    # Picture path
    img = cv2.imread(imageDir)
    coordXY_Tuple = []
    b = []

    def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            xy = "%d,%d" % (x, y)
            coordinate = (x, y)
            coordXY_Tuple.append(coordinate)
            # b.append(y)
            cv2.circle(img, (x, y), 1, (0, 0, 255), thickness=-1)
            cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                        1.0, (0, 0, 0), thickness=1)
            cv2.imshow("image", img)
            print(x, y)

    cv2.putText(img, f"Pick Coordinate USA, South_Africa,and Japan in Order", tuple(imageSize), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (0, 0, 0), thickness=1)
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
    cv2.imshow("image", img)
    cv2.waitKey(0)
    # print(a[0], b[0])
    # print(f'CV2-Coordinate:{a}')

    for i, country in enumerate(countryList):
        addCountryXY_hapticSuit(country, coordXY_Tuple[i][0], coordXY_Tuple[i][1])
        addCountryXY(country, coordXY_Tuple[i][0], coordXY_Tuple[i][1])


# for item in tempList:
#     print(item)
#     addCountry(item[0] ,item[1] ,item[2])
# def genPercValueGUI(mode, ):
#     if mode in countryList:
#         value = round(intensity * 100 / maxCountryCases[mode])
#         if value > 100:
#             value = 100
#         d = {"x": x, "y": y, "intensity": value}
#         return d
#     elif mode == 0:
#         value = round(intensity * 100 / maxCountryCases[country])
#
#         d = {"x": x, "y": y, "intensity": value}
#         return d
#     else:
#         print("Error: Use \"USA, JPN, ZAF, 0\"")


def genPathPoint(country, intensity, mode):
    x = countryPathPointCoordDic[country][0]
    y = countryPathPointCoordDic[country][1]
    # value = 0

    if mode in countryList:
        value = round(intensity * 100 / maxCountryCases[mode])
        if value > 100:
            value = 100
        d = {"x": x, "y": y, "intensity": value}
        return d
    elif mode == 0:
        value = round(intensity * 100 / maxCountryCases[country])

        d = {"x": x, "y": y, "intensity": value}
        return d
    else:
        print("Error: Use \"USA, JPN, ZAF, 0\"")

def genIntensity(intensity, mode):
    if mode in countryList:
        value = round(intensity * 100 / maxCountryCases[mode])
        if value > 100:
            value = 100
        return value
    elif mode == 0:
        value = round(intensity * 100 / maxCountryCases[country])
        return value
    else:
        print("Error: Use \"USA, JPN, ZAF, 0\"")

def main(mode):  # 0 = default(respective), "CountryISO" = setCountryMax as MaxIntensity
    global wait, millis
    print('======================== DEBUG MAIN ========================')

    # print(f'Test[{len()}]: {}')
    runCV2()
    initializeCovidWorldData()
    print(f'countryPathPointCoordDic ={countryPathPointCoordDic}')
    print(f'COVIDData[{len(CoVID_Data.keys())}]: {CoVID_Data}')
    print("MaxCountryCases=", maxCountryCases)

    # print(f'intensityList[{len(intensityList)}]: {intensityList}')

    print('======================== END DEBUG MAIN ========================')
    # wait = 0.2
    # millis = 200

    def test():
        pathPoint = [{"x": 0.5, "y": 0.5, "intensity": 100}]
        for i in range(5):
            player.submit_path("backFrame", "VestBack", pathPoint, millis)
            sleep(wait)

    # ================== Visualization CODE (matplotlib)===================
        # FIXME: Issue with running in .py environment
        # ----> See "Main-PathPoint(withGUI-JupyterOnly)" File for GUI Run
    # def initGUIMatPlotlib():
    #     import matplotlib.pyplot as plt
    #     fig, ax = plt.subplots(figsize=(6, 9))
    #     img = plt.imread(imageDir)
    #     ax.imshow(img)

    # ================== Main CODE Run===================
    player = haptic_player.HapticPlayer()
    sleep(0.1)
    sleep(2)

    test()  #For triggering BHaptic (prevent data loss)

    for i, (date, country_data) in enumerate(CoVID_Data.items()):
        # ==== Debug Skip =====
        if debugSkip != 0 and i <= debugSkip:
            continue

        # CoVID_Data Sample:
        # {'2020-01-23': {'USA': 0, 'ZAF': 0, 'JPN': 0},
        #   '2020-01-24': {'USA': 1, 'ZAF': 0, 'JPN': 0}, ...}

        pathPoint = []
        countryPercentDisplay = []
        for country, cases in country_data.items():
            pathPoint.append(genPathPoint(country, cases, mode))
            # For Text Display:
            countryPercentDisplay.append({country: (round(cases / maxCountryCases[country] * 100))})

        global displayText
        newlist = [""]
        # displayText = (f"#{i}| Date:{date}| data={country_data} | percentage={countryPercentDisplay} \n")
        displayText = (f"#{i}| Date:{date}")
        print(displayText)
        # window['output'].update(f"Date: {date}| DailyCases:{country_data}")
        # window.Refresh()
        # print(pathPoint)
        player.submit_path("backFrame", "VestBack", pathPoint, millis)
        sleep(wait)

    # window.close()


# ============ RUNTIME ==============

# main("JPN")
main(0)

#
# def test():
#         pathPoint = [{"x": 0.5, "y": 0.5, "intensity": 100}]
#         for i in range(5):
#             # player.submit_path("backFrame", "VestBack", pathPoint, millis)
#             player.submit_dot()
#             sleep(wait)
#
# test()