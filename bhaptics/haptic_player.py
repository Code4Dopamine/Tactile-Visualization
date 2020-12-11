import json
from websocket import create_connection

class HapticPlayer:
    def __init__(self):
        try:
            self.ws = create_connection("ws://localhost:15881/v2/feedbacks")
        except:
            print("Couldn't connect")
            return

    def register(self, key, file_directory):
        json_data = open(file_directory).read()

        data = json.loads(json_data)
        project = data["project"]

        layout = project["layout"]
        tracks = project["tracks"]

        request = {
            "Register": [{
                "Key": key,
                "Project": {
                    "Tracks": tracks,
                    "Layout": layout
                }
            }]
        }

        json_str = json.dumps(request)
        print("--- register[Output]: ---\n" + str(json_str))
        self.ws.send(json_str)

    def register2(self, key, file_directory):
        json_data = open(file_directory).read()

        data = json.loads(json_data)
        project = data["project"]

        layout = project["layout"]
        tracks = project["tracks"]

        request = {
            "Submit": [{
                "Key": key,
                "Project": {
                    "Tracks": tracks,
                    "Layout": layout
                }
            }]
        }

        json_str = json.dumps(request)
        print("--- register[Output]: ---\n" + str(json_str))
        self.ws.send(json_str)

    def submit_registered(self, key):
        submit = {
            "Submit": [{
                "Type": "key",
                "Key": key
            }]
        }

        json_str = json.dumps(submit)
        print("--- submit_registered[Output]: ---\n" + str(json_str))
        self.ws.send(json_str)

    def submit(self, key, frame):
        submit = {
            "Submit": [{
                "Type": "frame",
                "Key": key,
                "Frame": frame
            }]
        }

        json_str = json.dumps(submit)
        # self.print(json_str)
        
        # print("JsonStrType == ")
        # print(type(json_str))
        # print("--- submit[Output]: ---\n" +str(json_str))
        self.ws.send(json_str)

    def submit_dot(self, key, position, dot_points, duration_millis):
        
        # ==== Json (Complete) Output: ====
        # {"Submit": [{"Type": "frame", "Key": "frontFrame", "Frame": {"position": "VestFront", "dotPoints": [{"index": 1, "intensity": 100}, {"index": 4, "intensity": 100}, {"index": 8, "intensity": 100}], "durationMillis": 50}}]}

        front_frame = {
            "position": position,
            "dotPoints": dot_points,
            "durationMillis": duration_millis
        }
        self.submit(key, front_frame)
    # Modified Functions

    def submit_json(self, json):
        json_str = json.dumps(json)
        # self.print(json_str)
        print(str(json_str))
        self.ws.send(json_str)

    # def submit_path(self, key, position, xPos, yPos, intensity, duration_millis):
    def submit_path(self, key, position, path_points, duration_millis):
        """ player.submit_dot("frontFrame", "VestFront", [{"index": i, "intensity": 100}], durationMillis)
            (key, VestFront, [x: 0.5, y: 0.5, intensity: 100], 1000)
        """
        # if not isinstance(xPos, float):
        #     print("xPos Coordinate value not 'FLOAT'")
        # if not isinstance(yPos, float):
        #     print("yPos Coordinate value not 'FLOAT'")

        front_frame = {
            "position": position,
            # "pathPoints": [{"x": xPos, "y": yPos, "intensity": intensity}],
            "pathPoints": path_points,
            "durationMillis": duration_millis
        }
        self.submit(key, front_frame)
    

    ## ----------- CODE TO WORK ON -------------
    # def submit_tact(self, key, tact_File_Directory, (...)):
    #     # ==== Goal of Function ====
    #     # Parse ".tact" file and Play (like "Play Effect" in bHaptic Designer)

    #     # self.register(str(key),str(tact_File_Directory))

    #     #To Read .tact file
    #     json_data = open(tact_File_Directory).read()
    #     data = json.loads(json_data)
    #     project = data["project"]

    #     layout = project["layout"]
    #     tracks = project["tracks"]
    #     size = project["size"]

    #     bhapticVar1 = ???["???"]
    #     bhapticVar2 = ???["????"]

    #     #Open up ".tact" file and register (uploadToDevice)
    #     # self.register("bhapticVar1","bHapticVar")
    #     # self.submit_registered()
        

    #     # #--- Code For Parsing ".tact" File ---
    #     for i in rang(size):
    #         bhapticVar1 = ??[size]
    #         bhapticVar1 = ??[size]
    #         #? Play each "dot" for haptic feedback

    #     # #--- END OF Code For Parsing ".tact" File --- 

    #     json_str = json.dumps(json)
    #     self.ws.send(json_str)

    # END OF Modified Functions

    def __del__(self):
        self.ws.close()


 