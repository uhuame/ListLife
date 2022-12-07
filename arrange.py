import datetime,time
import threading

from tkinter import *
from tkinter import ttk
import tkinter.messagebox

import functions as f

class Main():
    
    def __init__(self, root):
        self.sleep_time = datetime.datetime(2022, 11, 30, hour=20)
        self.actives_list = ["数学","物理","历史","语文","英语","生物","其他"]
        self.root =root
        self.items = []
        self.items_added = []
        self.actives = False
        
        self.item_str = StringVar()
        self.left_time_str = StringVar()
        self.choicesvar = StringVar(value=self.actives_list)

        self.get_left_time()

        root.title("排课软件")

        self.mainframe = ttk.Frame(root, padding="5 5 12 3")
        self.mainframe.grid(column=0,row=0,sticky=(N,W,E,S))
        #root.rowconfigure(0,weight=1)

        self.item_str_set = StringVar()
        self.item_str_set_entry = ttk.Entry(self.mainframe, width=30, textvariable=self.item_str_set)

        item = f.load_file(self.items, self.items_added, self.mainframe, root)
        self.items = item[0]
        self.items_added = item[1]
        self.display()
        self.check_actives()
        #root.bind("<Return>", calculate)


    def get_item(self):
        #得到要完成的任务并绘制

        actives_index =self.activeslist.curselection()[0]
        value = [self.item_str_set.get(),\
                self.actives_list[actives_index]]
        item= f.handle_items(value, self.items, self.items_added, self.mainframe, root)
        self.items = item[0]
        self.items_added = item[1]
        #刷新按钮
        self.display_item_button()


    def get_left_time(self):
        """计算剩余时间"""
    
        self.end_time = self.sleep_time

        #设置初始时间
        now_time = datetime.datetime.now()
        now_time_H = int(now_time.strftime("%H"))
        now_time_M = int(now_time.strftime("%M"))
        now_time_S = int(now_time.strftime("%S"))
    
        #计算剩余时间
        left_time = self.end_time - \
            datetime.timedelta(minutes=now_time_M, hours=now_time_H, seconds=now_time_S) 

        self.left_time_str.set(left_time.strftime("%H:%M:%S"))
        #循环 
        self.root.after(1050, self.get_left_time)



    def display(self):
        self.item_str_set_entry\
        .grid(column=2, row=2, columnspan=3,sticky=(W, E))

        ttk.Label(self.mainframe, text="剩余时间")\
        .grid(column=1, row=1, sticky=W)
        ttk.Label(self.mainframe, text="格式: 名字 小时;")\
        .grid(column=1, row=2, sticky=(W))
        ttk.Label(self.mainframe, textvariable=self.left_time_str)\
        .grid(column=2, row=1, sticky=(W))
        ttk.Button(self.mainframe, text="提交", command=self.get_item)\
        .grid(column=5, row=2, sticky=W)
        
        self.activeslist = Listbox(self.mainframe, listvariable=self.choicesvar, height = 1)
        self.activeslist.grid(column=3, row=1, sticky=W)
#        ttk.Scrollbar(self.mainframe, orient=VERTICAL, command=self.activeslist.yview)rowspan=20
        self.display_item_button()

    def display_item_button(self):
        for i in range(len(self.items)):
            self.items[i].displayme(self.mainframe, i, self.actives)

    def check_actives(self): 

        actives_flag_list = []
        root.after(50, self.check_actives)

        del_flag = False
        for i in range(len(self.items)):
            actives_flag_list.append(self.items[i].actives)
            if self.items[i].done_flag:
                if self.items_added[i][2] != True :
                    self.items_added[i][2] = True
            if self.items[i].delete_flag:
                del_flag = True
                del_num = i

        if del_flag:
            self.items_added.remove([self.items[del_num].name,\
                    self.items[del_num].ticks, self.items[del_num].done_flag,\
                    self.items[del_num].actclass])
            f.save_file(self.items_added)
            del self.items[del_num]
            del_flag = False

        if True in actives_flag_list:
            actives_flag_index = actives_flag_list.index(True)
            if not self.actives :
                self.actives = True
                self.notstart_count(actives_flag_index)
                self.display_item_button()
        elif self.actives:
            self.actives = False
            self.display_item_button()
            notstartclass =""
            for item in self.items:
                if item.notstart_count > 3:
                    notstartclass += item.name+" "
            if notstartclass:
                tkinter.messagebox.showinfo(title='display_messagebox',\
                    message="太久没完成" + a)



#[true,flase]

    def notstart_count(self, actives_flag_index):
        startclass = self.items[actives_flag_index].actclass
        for item in self.items:
            if startclass == item.actclass:
                item.notstart_count = 0
            elif not item.done_flag:
                item.notstart_count +=1
root = Tk()
tha=Main(root)
root.mainloop()
