#############################################
#                                           #
#                  [MODULE]                 #
#                 Maid alarm                #
#                                           #
#############################################

from threading import Thread
from playsound import playsound
import datetime as dt
from PyQt5.Qt import QThread, QApplication, QObject

def create_connection():
    # Connect to the database
    import sqlite3
    from sqlite3 import Error
    database = "./resources/maidchan.db"
    conn = None
    sql = None
    try:
        conn = sqlite3.connect(database)
    except Error as e:
        print(e)
    finally:
        if conn:
            sql = conn.cursor()
    return (conn,sql)
class clock(Thread):
    def __init__(self):
        super(clock, self).__init__()
        # self.alarms = []
    def playSound(self):
        Thread(target=playsound, args=['resources/sounds/alarm.mp3']).start()
    def run(self):
        # lastLen = len(self.alarms)
        while(True):
            self.currentTime = dt.datetime.now()
            # Alarm triggered event handler ( Trigger when alarm timestamp = current timestamp)
            alarms = self.getAlarms()
            for alarm in alarms:
                id,hour,minute,timestamp,date = alarm
                if(self.currentTime.timestamp() >= timestamp):
                    # Removes the alarm from the database
                    self.playSound()
                    if(len(str(minute)) < 2):
                        minute = "0" + str(minute)
                    if(len(str(hour)) < 2):
                        hour = "0" + str(hour)
                    formattedAlarm = "Tal y como me pidió, \n le aviso que son las: %s:%s" % (hour,minute)
                    self.maidchan.notificationQueue.append(formattedAlarm)
                    self.maidchan.createNotification()
                    self.removeAlarm(timestamp)
            # New alarm event handler ( Trigger when new alarm is appended to the alarms list )
            # currentLen = len(self.alarms)
            # if(lastLen < currentLen):  # New alarm created
                # lastLen = currentLen
                # newAlarm = self.alarms[len(self.alarms)]
                # print("New alarm created: " + str(newAlarm))

    def addAlarm(self, **kargs):
        time = dt.datetime.now()
        time = time.combine(date=time.date(), time=dt.time(
            hour=int(kargs["hour"]), minute=int(kargs["minute"])))
        newAlarm = {
            "hour": time.hour,
            "minute": time.minute,
            "timestamp": time.timestamp(),
            "date": '"'+str(time.date())+'"'
        }
        # self.alarms.append(newAlarm)  # Append to the local memory
        # Append to the database
        conn,sql = create_connection()
        query = "INSERT INTO alarm (date,hour,minute,timestamp) VALUES (%s,%d,%d,%f)" % (
            newAlarm["date"], newAlarm["hour"], newAlarm["minute"], newAlarm["timestamp"])
        sql.execute(query)
        conn.commit()
        conn.close()

    def removeAlarm(self,timestamp):
        conn, sql = create_connection()
        query = "DELETE FROM alarm WHERE timestamp = %f" % (timestamp)
        sql.execute(query)
        conn.commit()
        conn.close()
    def getAlarms(self):
        conn, sql = create_connection()
        result = sql.execute("SELECT * FROM alarm")
        alarms = []
        for alarm in result:
            alarms.append(alarm)
        conn.close()
        return alarms
    def start(self, maid_thread):
        self.maidchan = maid_thread
        return super().start()

# a = clock()
# a.start()
# while(True):
#     print("Enter a new alarm:\n")
#     alarm = input()
#     alarmArray = alarm.split(":")
#     formatedTime = {
#         "hour": alarmArray[0],
#         "minute": alarmArray[1]
#     }
#     a.addAlarm(hour=formatedTime["hour"], minute=formatedTime["minute"])
