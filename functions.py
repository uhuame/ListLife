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

def handle_items(value, items, items_added, root):
    """处理项目"""
    item = []
    #能run就行讲究那么多干啥😅
    if value[-1] != ';':
        value +=';'
    for bi in value.split(";"):
        if bi:
            for i in bi.split():
                if i[-1] == ";":
                    i = i[:-1]
                item.append(i)
            items.append(Item(item[0], item[1], root))
            item=[]
    #将添加过的项目储存在变量里
    items_added += value
    save_file(items_added)
    return items, items_added

