import datetime,time
import threading

from tkinter import *
from tkinter import ttk

import functions as f

class Main():
    
    def __init__(self, root):
        self.sleep_time = datetime.datetime(2022, 11, 30, hour=21)
        self.root =root
        self.items = []
        self.items_added = []
        self.actives = False
        
        self.item_str = StringVar()
        self.left_time_str = StringVar()

        self.get_left_time()

        root.title("排课软件")

        self.mainframe = ttk.Frame(root, padding="5 5 12 3")
        self.mainframe.grid(column=0,row=0,sticky=(N,W,E,S))
        root.rowconfigure(0,weight=1)

        self.item_str_set = StringVar()
        self.item_str_set_entry = ttk.Entry(self.mainframe, width=30, textvariable=self.item_str_set)

        self.check_actives()
        self.display()

        item = f.load_file(self.items, self.items_added, root)
        self.items = item[0]
        self.items_added = item[1]
        self.display_item_button()
        #root.bind("<Return>", calculate)


    def get_item(self):
        #得到要完成的任务并绘制
        value = self.item_str_set.get() 
        item= f.handle_items(value, self.items, self.items_added, root)
        self.items = item[0]
        self.items_added = item[1]
        #刷新按钮
        self.display_item_button()


    def get_left_time(self):
        """计算剩余时间"""
    
        self.end_time =self.sleep_time
        #设置初始时间
        now_time = datetime.datetime.now()
        now_time_H = int(now_time.strftime("%H"))
        now_time_M = int(now_time.strftime("%M"))
        now_time_S = int(now_time.strftime("%S"))
    
        #计算剩余时间
        left_time = self.end_time - \
            datetime.timedelta(minutes=now_time_M,
                               hours=now_time_H, seconds=now_time_S)
        self.left_time_str.set(left_time.strftime("%H:%M:%S"))
        
        self.root.after(1000, self.get_left_time)

    def display(self):
        self.item_str_set_entry.grid(column=2, row=2, sticky=(W, E))

        ttk.Label(self.mainframe, text="剩余时间").grid(column=1, row=1, sticky=W)
        ttk.Label(self.mainframe, text="格式: 名字 小时;").grid(column=1, row=2, sticky=(W))
        ttk.Label(self.mainframe, textvariable=self.left_time_str).grid(column=2, row=1, sticky=(W))

        ttk.Button(self.mainframe, text="提交", command=self.get_item).grid(column=3, row=2, sticky=W)
        self.display_item_button()

    def display_item_button(self):
        for i in range(len(self.items)):
            self.items[i].displayme(self.mainframe, i, self.actives)

    def check_actives(self): 

        actives_list = []
        root.after(500, self.check_actives)

        del_flag = False
        for i in range(len(self.items)):
            actives_list.append(self.items[i].actives)
            if self.items[i].done_flag:
                if self.items_added[i][2] != True :
                    self.items_added[i][2] = True
            if self.items[i].delete_flag:
                del_flag = True
                del_num = i

        if del_flag:
            self.items_added.remove([self.items[del_num].name,\
                    self.items[del_num].need_time_H, self.items[del_num].done_flag])
            f.save_file(self.items_added)
            del self.items[del_num]
            del_flag = False

        if True in actives_list:
            if not self.actives :
                self.actives = True
                self.display_item_button()
        else:
            if self.actives:
                self.actives = False
                self.display_item_button()

root = Tk()
tha=Main(root)
root.mainloop()
