import datetime,time

from tkinter import *
from tkinter import ttk

class Item():
    def __init__(self, name, need_time, root):
        """初始化要完成的任务"""
        self.name = name

        self.root = root
        self.actives = False
        self.delete_flag = False
        self.need_time_H = need_time 
        self.need_time_str = StringVar()
        self.need_time = datetime.datetime(2022, 11, 30, hour=int(need_time))

        self.need_time_str.set(self.name + " " +self.need_time.strftime("%H:%M:%S"))

        self.button_str = StringVar()
        self.button_del_str = "删除"

    def displayme(self, frame, num_row, actives, now_time=""):
        """显示任务"""
        self.start_row=3
        row = self.start_row+num_row

        self.text = ttk.Label(frame, textvariable=self.need_time_str)
        self.text.grid(column=1, row=row, sticky=W)

        self.activess =actives
        self.button = ttk.Button(frame, textvariable=self.button_str, command=self.start)
        self.delete_button = ttk.Button(frame, text=self.button_del_str, command=self.delete)
        self.delete_button.grid(column=3, row=row, sticky=W)
        self.button.grid(column=2, row=row, sticky=W)

        if not actives:
            self.button_str.set("开始")
        else:
            self.button_str.set("已经有开始得了")
        self.check_left_time()

    def delete(self):
        self.text.destroy()
        self.delete_button.destroy()
        self.button.destroy()
        self.delete_flag = True

    def start(self):
        """开始任务"""
        now_time = datetime.datetime.now()
        if not self.activess and not self.actives:
            self.end_time =  now_time + datetime.timedelta(hours=int(self.need_time_H))
            self.get_left_need_time()
            self.actives =True

    def get_left_need_time(self):
        """得到剩余时间"""
        now_time = datetime.datetime.now()

        self.now_time_H = int(now_time.strftime("%H"))
        self.now_time_M = int(now_time.strftime("%M"))
        self.now_time_S = int(now_time.strftime("%S"))
        self.need_time = self.end_time - \
            datetime.timedelta(minutes=self.now_time_M,
                               hours=self.now_time_H, seconds=self.now_time_S)

        self.needtimestr = self.name +" " +self.need_time.strftime("%H:%M:%S")
        self.check_left_time()

        self.need_time_str.set(self.needtimestr)

    def check_left_time(self):
        if int(self.need_time.strftime("%H")) > 5:
            self.actives = False
            self.needtimestr=self.name +"时间结束 "
        if self.actives:
            self.root.after(1000,self.get_left_need_time)