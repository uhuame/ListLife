import json
import datetime,time
import threading

from items import *

def save_file(items_added, actives):
    filename = "./data.json"
    content = items_added[:]
    content.insert(0,actives)
    with open(filename, "w") as f_obj:
        json.dump(content, f_obj, sort_keys=True, indent=4)

def load_file(items, items_added, frame, root):
    filename = "./data.json"
    with open(filename) as f_obj:
        value = json.load(f_obj)
        actives_dict = value[0]
        value = value[1:]
        for i in value:
            items.append(Item(i, frame, root))
        items_added = value[:]
    return items, items_added, actives_dict

def handle_items(value, items, items_added, actives_dict, frame, root):
    """处理项目"""
    item = []
    value_str = value[0]
    actives = value[1]
    #能run就行讲究那么多干啥😅
    if value_str[-1] != ';':
        value_str +=';'
    for bi in value_str.split(";"):
        if bi:
            for i in bi.split():
                if i[-1] == ";":
                    i = i[:-1]
                item.append(i)
            item.append(False)
            item.append(actives)
            items.append(Item(item, frame, root))
            #将添加过的项目储存在变量里
            items_added.append(item)
            item=[]
    save_file(items_added, actives_dict)
    return items, items_added
