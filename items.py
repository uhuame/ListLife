import datetime,time

from tkinter import *
from tkinter import ttk

from playsound import playsound

class Item():
    def __init__(self, itemattr, settings, frame, root):
        """初始化要完成的任务"""
        self.settings    = settings
        self.itemattr    = itemattr#方便删除
        self.name        = itemattr[0]
        self.ticks       = int(itemattr[1])
        self.done_flag   = itemattr[2]
        self.actclass    = itemattr[3]
        self.ticks_past  = itemattr[4] #已经度过的单位时
        self.name_display= self.actclass + self.name 
        self.root        = root
        self.actives     = False
        self.delete_flag = False
        self.yes_flag    = False
        self.break_flag  = False
        self.hide_flag   = False
        self.save_flag   = False

        self.time_track = self.settings.time_track

        self.button_str = StringVar()
        self.button_del_str = StringVar(value="删除")
        self.need_time_str = StringVar()

        self.init_needtime()
        self.button = ttk.Button(frame, textvariable=self.button_str, command=self.start)
        self.delete_button = ttk.Button(frame, textvariable=self.button_del_str, command=self.delete)
        self.cancel_button = ttk.Button(frame, text="取消", command=self.cancel)
        self.delay_button = ttk.Button(frame, text="贪睡时间", command=self.delay)

        self.text_name = ttk.Label(frame, text=self.name_display)
        self.text_time = ttk.Label(frame, textvariable=self.need_time_str)

    def init_needtime(self,need_time_minute=''):
        ''' 初始化needtime以及一系列东西'''
        ticks = int(self.ticks) - self.ticks_past

        need_time = int(ticks) * self.time_track / 60

        self.need_time_minute = int( (need_time - int(need_time)) * 60 )
        self.need_time_H = int(need_time)

        self.need_time = datetime.datetime(2022, 11, 30, hour=self.need_time_H,minute=self.need_time_minute)
        self.break_time = datetime.datetime(2022, 11, 30, hour=self.need_time_H,minute=self.need_time_minute)

        self.need_time_str.set(str(ticks) )

    def displayme(self, num_row, actives, now_time=""):
        """配置显示任务"""
        self.start_row=3
        self.row = self.start_row+num_row
        self.activess =actives
        if not actives:
            self.button_str.set("开始")
        else:
            self.button_str.set("已经有开始得了")
#        self.check_left_time()

    def delete(self):
        if not self.yes_flag:
            self.button_del_str.set("你确定么？")
            self.cancel_button.grid(column=6, row=self.row, sticky=W)
            self.yes_flag = True
            self.actives=False
        else:
            self.text_name.destroy()
            self.text_time.destroy()
            self.delete_button.destroy()
            self.delay_button.destroy()
            self.cancel_button.destroy()
            self.button.destroy()
            self.itemattr = [
                    self.name,
                    self.ticks,
                    self.done_flag,
                    self.actclass,
                    self.ticks_past
                    ]
            self.save_flag = True
            self.delete_flag = True

    def display(self):
        self.text_name.grid_configure(column=1, row=self.row, sticky=W)
        self.text_time.grid_configure(column=2, row=self.row, sticky=W)
        self.delete_button.grid(column=5, row=self.row, sticky=W)
        self.button.grid(column=3, row=self.row, sticky=W)
        if self.done_flag:
            self.delay_button.grid_configure(column=4, row=self.row, sticky=W)
        self.hide_flag = False
        self.check_left_time()
        
    def hide(self):
        self.text_time.grid_remove()
        self.text_name.grid_remove()
        self.delete_button.grid_remove()
        self.cancel_button.grid_remove()
        self.delay_button.grid_remove()
        self.button.grid_remove()
        self.hide_flag = True

    def delay(self, need_time_minute=""):
        if need_time_minute:
            self.time_track = need_time_minute 
            self.ticks_past = 0
        else:
            self.ticks+=1
        self.init_needtime(need_time_minute)
        """
        self.need_time_H = 0
        self.need_time_minute=need_time_minute
        self.need_time_str.set(self.name_display + " " +self.need_time.strftime("%H:%M:%S"))
        """
        self.done_flag = False
        #self.check_left_time() # 用于在延迟后刷新标签

    def fuc(self, need_time_H, need_time_minute):
        "得到需要的时间"
        self.now_time = datetime.datetime.now()
        self.end_time =  self.now_time + datetime.timedelta(hours=need_time_H,minutes=need_time_minute) # type datetime
        self.breaktime =  self.now_time + datetime.timedelta(minutes=self.time_track) 
        #获得距离休息的时间 使用单独的变量是为了方便提醒项目改时间

        self.now_time = datetime.datetime.now()

        self.now_time_H = int(self.now_time.strftime("%H"))
        self.now_time_M = int(self.now_time.strftime("%M"))
        self.now_time_S = int(self.now_time.strftime("%S"))
      
        self.now_time =  datetime.timedelta(minutes=self.now_time_M,
                               hours=self.now_time_H, seconds=self.now_time_S)
        #end_time datetime-timedelta
        self.need_time = self.end_time - self.now_time

    def cancel(self):
            self.yes_flag = False
            self.button_del_str.set("删除")
            self.cancel_button.grid_remove()

    def start(self):
        """开始任务"""
        if not self.activess and not self.actives and not self.done_flag:
            self.fuc(self.need_time_H, self.need_time_minute)
            self.needtimestr="完成"
            playsound("Sounds/startsound.mp3", False)
            self.actives =True #必须在下面那个之前
            self.check_left_time()#调用循环
        else:
            playsound("Sounds/badsound.wav", False)

    def check_left_time(self):

        if int(self.ticks) <= self.ticks_past or self.done_flag:
            self.actives = False
            self.done_flag = True
            self.needtimestr="完成"
            self.need_time_str.set(self.needtimestr)

            self.save_flag = True#传递保存标志让arrange的函数保存

        if int(self.break_time.strftime("%H")) > 5 or self.break_flag:
            #当在休息(包括开始结束进行中时)执行下列
            if int(self.break_time.strftime("%H")) > 5 and self.break_flag :
                #如果正要开始项目执行下列
                self.break_flag = False
                self.breaktime =  self.breaktime + datetime.timedelta(minutes=self.time_track)
                playsound("Sounds/startsound.mp3", False)

            elif not self.break_flag :
                #如果正要开始休息执行下列
                playsound("Sounds/restsound.wav", False)
                self.break_flag = True
                self.end_time =  self.end_time + datetime.timedelta(minutes=self.settings.rest_time)
                self.breaktime =  self.breaktime + datetime.timedelta(minutes=self.settings.rest_time)
                self.ticks_past += 1 #添加过去的时间
                self.save_flag = True
            self.needtimestr="休息了" + self.break_time.strftime("%M:%S")

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

        self.needtimestr = '剩下：' + left_time.strftime("%H:%M:%S")+"还有："+ self.break_time.strftime("%M:%S")
        self.check_left_time()
        self.need_time_str.set(self.needtimestr)
