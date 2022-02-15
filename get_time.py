from gps import *
import threading
import datetime
import json
import time
import os
# might use gpsd instead; look into later

class gps_poll():   #threaded GPS polling class
    def __init__(): #create the thread
        threading.Thread.__init__(self)
        self.session = gps(mode=WATCH_ENABLE)
        self.current_value = None

    def get_current_value(self):    #get the current data from GPSD
        return self.current_value

    def run(self):
        try:
            while True:
                self.current_value = self.session.next()
                time.sleep(1)
        except StopIteration:
            printf("Thread interrupted via StopIteration")

if __name__ == "__main__":
    gpsp = gps_poll()
    try:
        gpsp.start()    #start thread
        while True:     #run forever until Ctrl-C
            report = gpsp.get_current_value()   #gets data from gpsd
            try:
                if report.keys()[0] == "epx":
                    file = open("current_gps_data.txt", "w")
                    utc_time = report["time"]   #time in UTC
                    dt = datetime.datetime.strptime(utc_time, "%Y%m%dT%H%M")    #convert to Unix time
                    unix_time = dt.timestamp()
                    json_str = json.dumps({"lat":f"{report["lat"]}", "lon":f"{report["lon"]}", "unix_time":f"{unix_time}"})
                    file.write(json_str)    #write json to file to be read later
                time.sleep(2)
            except(AttributeError, KeyError):
                print("Error occured getting the values")
            time.sleep(2)
    except(KeyboardInterrupt, SystemExit):
        print("Killing the GPS thread...")
        gpsp.running = False
        gpsp.join()
    print("Exiting...")
