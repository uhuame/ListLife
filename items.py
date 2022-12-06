import datetime,time

from tkinter import *
from tkinter import ttk

from playsound import playsound

class Item():
    def __init__(self, itemattr , actclass, frame,root):
        """初始化要完成的任务"""
        self.name = itemattr[0]

        self.actclass = actclass
        self.notstart_count = 0

        self.root = root
        self.actives = False
        self.delete_flag = False
        self.yes_flag = False
        self.break_flag = False
        self.done_flag = itemattr[2]        

        # 记录单位时间的次数 方便删除时使用
        self.ticks = itemattr[1]

        need_time = int(itemattr[1]) * 30 / 60

        self.need_time_minute = int( (need_time - int(need_time)) * 60 )

        self.need_time_H = int(need_time)
        self.need_time_str = StringVar()

        self.need_time = datetime.datetime(2022, 11, 30, hour=self.need_time_H,minute=self.need_time_minute)
        self.break_time = datetime.datetime(2022, 11, 30, hour=self.need_time_H,minute=self.need_time_minute)

        self.need_time_str.set(self.name + " " +self.need_time.strftime("%H:%M:%S"))

        self.button_str = StringVar()
        self.button_del_str = StringVar()
        self.button_del_str.set("删除")

        self.button = ttk.Button(frame, textvariable=self.button_str, command=self.start)
        self.delete_button = ttk.Button(frame, textvariable=self.button_del_str, command=self.delete)
        self.cancel_button = ttk.Button(frame, text="取消", command=self.cancel)
        self.delay_button = ttk.Button(frame, text="贪睡时间", command=self.delay)
        self.text = ttk.Label(frame, textvariable=self.need_time_str)

    def displayme(self, frame, num_row, actives, now_time=""):
        """显示任务"""
        self.start_row=3
        self.row = self.start_row+num_row

        self.activess =actives

        self.delete_button.grid(column=5, row=self.row, sticky=W)
        self.button.grid(column=2, row=self.row, sticky=W)
        self.text.grid(column=1, row=self.row, sticky=W)

        if not actives:
            self.button_str.set("开始")
        else:
            self.button_str.set("已经有开始得了")

        self.check_left_time()

    def delete(self):
        if not self.yes_flag:
            self.button_del_str.set("你确定么？")
            self.cancel_button.grid(column=6, row=self.row, sticky=W)
            self.yes_flag = True
            self.actives=False
        else:
            self.text.destroy()
            self.delete_button.destroy()
            self.cancel_button.destroy()
            self.delay_button.destroy()
            self.button.destroy()
            self.delete_flag = True

    def delay(self):
            self.done_flag = False
            self.need_time_str.set(self.name + " " +self.need_time.strftime("%H:%M:%S"))

    def cancel(self):
            self.yes_flag = False
            self.button_del_str.set("删除")
            self.cancel_button.grid_remove()

    def start(self):
        """开始任务"""
        now_time = datetime.datetime.now()
        if not self.activess and not self.actives:
            playsound("Sounds/31b3533e-179ccf9d194.mp3", False)
            self.end_time =  now_time + datetime.timedelta(hours=self.need_time_H,minutes=self.need_time_minute) # type datetime
            self.breaktime =  now_time + datetime.timedelta(minutes=30)
            self.get_left_need_time()
            self.actives =True

    def check_left_time(self):

        if int(self.need_time.strftime("%H")) > 5 or self.done_flag:
            self.delay_button.grid(column=4, row=self.row, sticky=W)
            self.actives = False
            self.done_flag = True
            self.needtimestr=self.name +"完成 "
            self.need_time_str.set(self.needtimestr)

        if int(self.break_time.strftime("%H")) > 5 or self.break_flag:
            if int(self.break_time.strftime("%H")) > 5 and self.break_flag :
                self.break_flag = False
                self.breaktime =  self.breaktime + datetime.timedelta(minutes=30)
                playsound("Sounds/31b3533e-179ccf9d194.mp3", False)
            elif not self.break_flag :
                playsound("Sounds/restsound.wav", False)
                self.break_flag = True
                self.end_time =  self.end_time + datetime.timedelta(minutes=10)
                self.breaktime =  self.breaktime + datetime.timedelta(minutes=10)
            self.needtimestr=self.name +"休息了" + self.break_time.strftime("%M:%S")

        if self.actives:
            self.root.after(1000,self.get_left_need_time)

    def get_left_need_time(self):
        """得到剩余时间"""

        self.now_time = datetime.datetime.now()
        sleep_time = datetime.datetime(2022, 11, 30, hour=20)

        self.now_time_H = int(self.now_time.strftime("%H"))
        self.now_time_M = int(self.now_time.strftime("%M"))
        self.now_time_S = int(self.now_time.strftime("%S"))
      
        self.now_time =  datetime.timedelta(minutes=self.now_time_M,
                               hours=self.now_time_H, seconds=self.now_time_S)
        #end_time datetime-timedelta
        self.need_time = self.end_time - self.now_time
        self.break_time = self.breaktime - self.now_time

        int_time = int(self.need_time.strftime("%H"))
        int_time_M = int(self.need_time.strftime("%M"))
        int_time_S = int(self.need_time.strftime("%S"))

        now_need_time =  datetime.timedelta(minutes=self.now_time_M+int_time_M,
                               hours=self.now_time_H+int_time, seconds=self.now_time_S+int_time_S)
        #now_need_time = end_time
        #datetime-timedelta
        left_time = sleep_time - now_need_time

        self.needtimestr = self.name +" " +self.need_time.strftime("%H:%M:%S")+' 剩余'+left_time.strftime("%H:%M:%S")+"距离休息还有："+ self.break_time.strftime("%M:%S")
        self.check_left_time()
        self.need_time_str.set(self.needtimestr)
