import datetime,time

class Settings():
    def __init__(self):
        #一天的结束的时间
        self.sleep_time = datetime.datetime(2022, 11, 30, hour=21)
        #一个周期的时长
        self.time_track = 50
        #多少个事件未作时提醒
        self.count = 10
        #休息时间
        self.rest_time = 10
