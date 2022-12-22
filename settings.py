import datetime,time

class Settings():
    def __init__(self):
        #一天的结束的时间
        self.sleep_time = datetime.datetime(2022, 11, 30, hour=20)
        #一个周期的时长
        self.time_track = 1
        #多少个事件未作时提醒
        self.count = 10
