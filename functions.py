import json
import datetime,time
import threading

from items import *

def save_file(content):
    filename = "data.json"
    with open(filename, "w") as f_obj:
        json.dump(content, f_obj)

def load_file(items, items_added, root):
    filename = "data.json"
    with open(filename) as f_obj:
        value = json.load(f_obj)
    tmp = handle_items(value, items, items_added, root)
    return tmp

def get_left_time(end_time):
    """计算剩余时间"""

    #设置初始时间
    now_time = datetime.datetime.now()
    now_time_H = int(now_time.strftime("%H"))
    now_time_M = int(now_time.strftime("%M"))
    now_time_S = int(now_time.strftime("%S"))

    #计算剩余时间
    left_time = end_time - \
        datetime.timedelta(minutes=now_time_M,
                           hours=now_time_H, seconds=now_time_S)
    return left_time.strftime("%H:%M:%S")

def handle_items(value, items, items_added, root):
    """处理项目"""
    item = []
    #能run就行讲究那么多干啥😅
    for bi in value.split(";"):
        print(bi)
        if bi:
            for i in bi.split():
                if i[-1] == ";":
                    i = i[:-1]
                else:
                    bi += ";"
                item.append(i)
            items.append(Item(item[0], item[1], root))
            item=[]
    #将添加过的项目储存在变量里
    items_added += value
    save_file(items_added)
    return items, items_added

