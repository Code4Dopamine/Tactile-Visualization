# =================================================================================
import cv2
# import numpy as np
import sqlite3
from bhaptics import haptic_player
from time import sleep
import PySimpleGUI as sg

pathPointList = []
countryCoordinateDic = {}
# tempList = [("USA", 160, 539), ("JPN", 185, 306), ("BRA", 315, 260)]
countryList = ["USA", "ZAF", "JPN"]
sampleData = ['USA', '2020-01-23', '0']
maxCountryCases = {}  # USA, JPN, ZAF

imageSize = [480, 699]

# Testing Only
dateList = []
CoVID_Data = {}
intensityList = {"USA": [], "ZAF": [], "JPN": []}
selection = "date, iso_code, new_cases"

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

    print("MaxCountryCases=", maxCountryCases)

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
    newX = round(x / imageSize[0], 3)
    newY = round(y / imageSize[1], 3)

    d = {str(name): [newX, newY]}
    # print(f'{d} -- Type:{type(d)}')
    countryCoordinateDic.update(d)


def runCV2():
    # import cv2
    # import numpy as np

    # Picture path
    img = cv2.imread("CSVData/world2.jpg")
    a = []
    b = []

    def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            xy = "%d,%d" % (x, y)
            coordinate = (x, y)
            a.append(coordinate)
            # b.append(y)
            cv2.circle(img, (x, y), 1, (0, 0, 255), thickness=-1)
            cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                        1.0, (0, 0, 0), thickness=1)
            cv2.imshow("image", img)
            print(x, y)

    cv2.putText(img, f"Pick Coordinate USA, South_Africa,and Japan in Order", (0, 690), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (0, 0, 0), thickness=1)
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
    cv2.imshow("image", img)
    cv2.waitKey(0)
    # print(a[0], b[0])
    # print(f'CV2-Coordinate:{a}')

    for i, country in enumerate(countryList):
        addCountryXY_hapticSuit(country, a[i][0], a[i][1])


# for item in tempList:
#     print(item)
#     addCountry(item[0] ,item[1] ,item[2])

def genPathPoint(country, intensity, mode):
    x = countryCoordinateDic[country][0]
    y = countryCoordinateDic[country][1]
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


def main(mode):  # 0 = default(respective), "CountryISO" = setCountryMax as MaxIntensity
    print('======================== BEGIN MAIN ========================')

    # print(f'Test[{len()}]: {}')
    runCV2()
    initializeCovidWorldData()
    print(f'CountryCoordinateDic ={countryCoordinateDic}')
    print(f'COVIDData[{len(CoVID_Data.keys())}]: {CoVID_Data}')

    # for checking only
    # print(f'intensityList[{len(intensityList)}]: {intensityList}')

    player = haptic_player.HapticPlayer()
    sleep(0.1)
    sleep(2)

    wait = 0.2
    millis = 200

    def test():
        pathPoint = [{"x": 0.5, "y": 0.5, "intensity": 100}]
        for i in range(5):
            player.submit_path("backFrame", "VestBack", pathPoint, millis)
            sleep(wait)

    # ================== GUI CODE ===================

    #     layout = [[sg.Text('Persistent window')],
    #               # [sg.Input()],
    #               [sg.Text("Data Display:"), sg.Text("(None)", size=(40, 1), key='output')],
    #               [sg.Button('Start'),sg.Exit()]]
    #     # sg.Button('Quit'),
    #     window = sg.Window('Window that stays open', layout)
    # # ================== END GUI CODE ===================
    #     event,stuff = window.read()
    test()

    for i, (date, country_data) in enumerate(CoVID_Data.items()):

        # ==== Debug Skip =====
        # if i <= 300:
        #     continue

        # CoVID_Data Sample:
        # {'2020-01-23': {'USA': 0, 'ZAF': 0, 'JPN': 0},
        #   '2020-01-24': {'USA': 1, 'ZAF': 0, 'JPN': 0}, ...}

        # displayTK():
        # TODO: Write TK() to display "Actual Data"
        # window['output'].update()

        pathPoint = []
        countryPercentDisplay = []
        for country, cases in country_data.items():
            pathPoint.append(genPathPoint(country, cases, mode))
            # For Text Display:
            countryPercentDisplay.append({country: (round(cases / maxCountryCases[country] * 100))})

        global displayText
        newlist = [""]
        displayText = (f"Date:{date}| data={country_data} | percentage={countryPercentDisplay} \n")
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

# PySimple GUI Stuff
# def gui_run2():
#     layout = [[sg.Text('Display Window')],
#               [sg.Input()],
#               [sg.Text("Initializing....",size=(40, 1),auto_size_text=True,key='update')],
#               [sg.Button('Read'), sg.Exit()]]
#
#     window = sg.Window('Window that stays open', layout)
#
#     while True:
#         event, values = window.read()
#         window['update'].update(displayText)
#         window.Refresh()
#         print(event, values)
#         if event in (sg.WIN_CLOSED, 'Exit'):
#             break
#
#     window.close()


# def gui_run():
#
#     layout = [[sg.Text('Custom Text')],
#               [sg.ProgressBar(1, orientation='h', size=(20, 20), key='progress')],
#               [sg.Text("(None)", size=(40, 1), key='display', auto_size_text=True)],
#               [sg.Exit()]
#               ]
#     # This Creates the Physical Window
#     window = sg.Window('Window Title', layout).Finalize()
#     progress_bar = window.FindElement('progress')
#     text = window.FindElement('display')
#
#     counter = 0
#
#     # This Updates the Window
#     # progress_bar.UpdateBar(Current Value to show, Maximum Value to show)
#     while True:
#         event, values = window.read()
#         progress_bar.UpdateBar(counter, 10000)
#         window['display'].update(displayText)
#         counter += 1
#         if event is None:
#             window['display'].update(displayText)
#         if event in (sg.WIN_CLOSED, 'Exit'):
#             break
#     # # adding time.sleep(length in Seconds) has been used to Simulate adding your script in between Bar Updates
#     # sleep(.5)
#     #
#     # progress_bar.UpdateBar(1, 5)
#     # text.update(f"counter:={counter}")
#     # counter += 1
#     # sleep(.5)
#     #
#     # progress_bar.UpdateBar(2, 5)
#     # sleep(.5)
#     #
#     # progress_bar.UpdateBar(3, 5)
#     # sleep(.5)
#     #
#     # progress_bar.UpdateBar(4, 5)
#     # sleep(.5)
#     #
#     # progress_bar.UpdateBar(5, 5)
#     # sleep(.5)
#     # # I paused for 3 seconds at the end to give you time to see it has completed before closing the window
#     # sleep(3)
#     #
#     # # This will Close The Window
#     window.Close()
#
# def gui_run3():
#     while True:
#         print(f"========== {displayText} ==================")
#         sleep(1)
#
# from threading import Thread
# thread1 = Thread(target=gui_run)
# # thread2 = Thread(target=main, args=(0,))
# thread1.start()
# # thread2.start()
# main(0)


# ================ THREADING TEST =================
# from threading import Thread
# from playsound import playsound
#
# def play_sound():
#     playsound('welcome.mp3')
#
# thread = Thread(target=play_sound)
# thread.start()


# import PySimpleGUI as sg
#
# layout = [[sg.Text('Persistent window')],
#           [sg.Input()],
#           [sg.Button('Read'), sg.Exit()]]
#
# window = sg.Window('Window that stays open', layout)
#
# while True:
#     event, values = window.read()
#     print(event, values)
#     if event in (sg.WIN_CLOSED, 'Exit'):
#         break
#
# window.close()