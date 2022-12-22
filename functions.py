import json
import datetime,time
import threading

from items import *

def save_file(items_added, actives):
    #当修改data.json储存的结构时不用管这里 去修改handle_items 
    filename = "./data.json"
    content = items_added[:]
    content.insert(0,actives)
    with open(filename, "w") as f_obj:
        json.dump(content, f_obj, sort_keys=True, indent=4)

def load_file(items, items_added, settings, frame, root):
    filename = "./data.json"
    with open(filename) as f_obj:
        value = json.load(f_obj)
        actives_dict = value[0]
        value = value[1:]
        for i in value:
            items.append(Item(i, settings, frame, root))
        items_added = value[:]
    return items, items_added, actives_dict

def handle_items(value, items, items_added, settings, actives_dict, frame, root):
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
                    i = int(i[:-1])
                item.append(i)
            item[-1] = int(item[-1])#将项目次数变为整数
            item.append(False)
            item.append(actives)
            item.append(0)#已经度过的单位时间
            items.append(Item(item, settings, frame, root))
            #将添加过的项目储存在变量里
            items_added.append(item)
            item=[]
    save_file(items_added, actives_dict)
    return items, items_added
