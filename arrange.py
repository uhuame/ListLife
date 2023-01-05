import datetime,time
import threading

from tkinter import *
from tkinter import ttk
import tkinter.messagebox

import items as ITTE

import functions as f
from settings import Settings

class Main():
    
    def __init__(self, root):
        self.settings = Settings()
        self.sleep_time = self.settings.sleep_time
        self.root =root
        self.items = []
        self.items_added = []
        self.actives = False

        self.mainframe = ttk.Frame(root, padding="5 5 12 3")
        self.mainframe.grid(column=0,row=0,sticky=(N,W,E,S))

        item = f.load_file(self.items, self.items_added, self.settings, self.mainframe, root)
        self.items = item[0]
        self.items_added = item[1]
        self.actives_dict = item[2]

        self.actives_list = []
        for i in self.actives_dict.keys():
            self.actives_list.append(i)

        self.item_str = StringVar()
        self.left_time_str = StringVar()
        self.hide_str = StringVar(value="隐藏")
        self.notstartclass_str = StringVar()
        #self.choicesvar = StringVar(value=self.actives_list)
        self.choicesvar = StringVar(value="请键入一个活动的名称")

        self.get_left_time()

        root.title("排课软件")

        #root.rowconfigure(0,weight=1)

        self.reminditem = ITTE.Item(["提醒", 1, False, "debug", 0], self.settings, self.mainframe, root)
        self.reminditem.activess = False
        self.reminditem.actives = False
        self.reminditem.delay(15)
        self.reminditem.start()

        self.item_str_set = StringVar()
        self.item_str_set_entry = ttk.Entry(self.mainframe, width=30, textvariable=self.item_str_set)

        self.display()
        self.check_actives()

        #root.bind("<Return>", calculate)

    def get_item(self):
        #得到要完成的任务并绘制
#        actives_index = self.activeslist.curselection()[0]
        #itemactclass = self.actives_list[actives_index]
        itemactclass = self.choicesvar.get()

        if itemactclass not in self.actives_dict:
            self.actives_dict[itemactclass] = 0
            self.actives_list.append(itemactclass)
            self.activeslist['values'] = self.actives_list

        value = [self.item_str_set.get(),\
                itemactclass]
        item= f.handle_items(value, self.items, self.items_added, self.settings, self.actives_dict, self.mainframe, root)
        self.items = item[0]
        self.items_added = item[1]

        #刷新按钮
        self.display_item_button()
        self.items[-1].display()


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
        .grid(column=3, row=2, columnspan=3,sticky=(W, E))

        ttk.Label(self.mainframe, text="剩余时间")\
        .grid(column=1, row=1, sticky=W)
        ttk.Label(self.mainframe, text="格式: 名字 小时;")\
        .grid(column=1, row=2, sticky=(W))
        ttk.Label(self.mainframe, textvariable=self.left_time_str)\
        .grid(column=3, row=1, sticky=(W))
        ttk.Button(self.mainframe, text="提交", command=self.get_item)\
        .grid(column=5, row=2, sticky=W)
        ttk.Button(self.mainframe, textvariable=self.hide_str, command=self.hide_done)\
        .grid(column=5, row=1, sticky=W)
        ttk.Label(self.mainframe, textvariable=self.notstartclass_str)\
        .grid(column=2, row=2, sticky=W)
        
        #self.activeslist = Listbox(self.mainframe, listvariable=self.choicesvar, height = 1)
        #self.activeslist.grid(column=3, row=1, sticky=W)
        self.activeslist = ttk.Combobox(self.mainframe, text=self.choicesvar, height = 5)
        self.activeslist.grid(column=4, row=1, sticky=W)
        self.activeslist['values'] = self.actives_list

        #self.daylist = ttk.Combobox(self.mainframe, text=self.choicesvar, height = 5)
        #self.daylist.grid(column=2, row=2, sticky=W)
        #self.daylist['values'] = self.day_list

        #self.mouthlist = ttk.Combobox(self.mainframe, text=self.choicesvar, height = 5)
        #self.mouthlist.grid(column=2, row=1, sticky=W)
        #self.mouthlist['values'] = self.mouth_list

        self.display_item_button()
        for item in self.items:
            item.display()

    def hide_done(self):
        """隐藏已经完成的项目"""
        for item in self.items:
            if item.hide_flag:
                item.display()
                self.hide_str.set("隐藏")
            elif item.done_flag :
                item.hide()
                self.hide_str.set("显示")

    def display_item_button(self):
        for i in range(len(self.items)):
            self.items[i].displayme(i, self.actives)

    def check_actives(self): 

        actives_flag_list = []
        root.after(500, self.check_actives)

        del_flag = False
        # 获得完成标志与删除标志需要保存标志
        for i in range(len(self.items)):
            actives_flag_list.append(self.items[i].actives)

            #如果保存标志为真则保存
            if self.items[i].save_flag:
                self.items_added[i][0] = self.items[i].name        
                self.items_added[i][1] = self.items[i].ticks       
                self.items_added[i][2] = self.items[i].done_flag   
                self.items_added[i][3] = self.items[i].actclass    
                self.items_added[i][4] = self.items[i].ticks_past  
                f.save_file(self.items_added, self.actives_dict)
                self.items[i].save_flag = False

            if self.items[i].delete_flag:
                del_flag = True
                del_num = i

        if del_flag:
            self.items_added.remove(self.items[del_num].itemattr)
            del self.items[del_num]
            del_flag = False
            f.save_file(self.items_added, self.actives_dict)

        if True in actives_flag_list:
            if not self.actives :
                self.actives_flag_index = actives_flag_list.index(True)
                self.actives = True
                self.display_item_button()
                self.reminditem.actives=False
        elif self.actives:
            self.notstart_count(self.actives_flag_index)
            self.actives = False
            self.display_item_button()
            notstartclass =""
            #提醒
            self.reminditem.delay(15)
            self.reminditem.start()

            for key, value in self.actives_dict.items():
                if value >= self.settings.count:
                    notstartclass += key+" :"
                    for item in self.items:
                        if not item.done_flag:
                            if item.actclass == key:
                                notstartclass += item.name + "\n"
            if notstartclass:
                tkinter.messagebox.showinfo(title='display_messagebox',\
                    message="太久没完成" + notstartclass)
                self.notstartclass_str.set("太久没完成" + notstartclass)

        #print("休息:"+self.reminditem.break_time.strftime("%M:%S"))
        #print("剩余:"+self.reminditem.need_time.strftime("%M:%S"))

        if self.reminditem.done_flag:
            self.reminditem.start()
            test =tkinter.messagebox.askquestion(title='display_messagebox', message="请指定下一个项目")
            if test == 'yes':
                self.reminditem.delay(1)
                self.reminditem.break_flag = False
                self.reminditem.start()

#[true,flase]
    def notstart_count(self, actives_flag_index):
        startclass = self.items[actives_flag_index].actclass
        for i in self.actives_dict.keys():
            self.actives_dict[i] += 1
        #此行必在上下面 (将开始的类的计数归零)
        self.actives_dict[startclass] = 0
        print(self.actives_dict)
        f.save_file(self.items_added, self.actives_dict)

root = Tk()
tha=Main(root)
root.mainloop()
