import json
import re

FILE_NAME="bookmarks-storage.json"
"""
    STORAGE STRUCTURE :
    {
        'chat_id_1' : {
            "topic_1" : ['url1', 'url2'],
            "topic_2" : ['url1', 'url2'],
        },
        ......
        'chat_id_n' : {
            "topic_1" : ['url1', 'url2'],
            .....
            "topic_n" : ['url1', 'url2'],
        },
    }
"""

#########################################################
############### READ \ WRITE JSON STORAGE ###############


def read():
    with open(FILE_NAME, 'r') as infile:
        data = json.load(infile)
        print('[DEBUG-storage_controller.read] - data in storage', data)
    return data


def write(data_new):
    with open(FILE_NAME, 'w') as out_json:
        json.dump(data_new, out_json)
        print('[DEBUG-storage_controller.write] - data to storage', data_new)


def read_by_chat_id(id):
    with open(FILE_NAME, 'r') as infile:
        data = json.load(infile)
    print('[DEBUG-storage_controller.read_by_chat_id] - DATA READ BY CHAT ID: ', data[id])
    return data[id]


def check_if_id_exists(id):
    data_l = read()
    print(type(data_l))
    print(type(id))
    if str(id) in data_l:
        print('[DEBUG-storage_controller.check_if_id_exists] - ID EXISTS')
        return True
    else:
        print('[DEBUG-storage_controller.check_if_id_exists] - ID NOT EXISTS')
        return False

def check_if_topic_exists(id, topic):
    data_storage = read()
    if topic in data_storage[str(id)]:
        print('[DEBUG-storage_controller.check_if_topic_exists] - TOPIC {} ALREADY EXISTS'.format(topic))
        return True
    else:
        print('[DEBUG-storage_controller.check_if_topic_exists] - TOPIC {} NOT EXISTS'.format(topic))
        return False


############## ADD
def add_chat_id_to_storage(id):
    data_new= {"{}".format(id):{}}
    print('[DEBUG-storage_controller.add_chat_id_to_storage] - new id to storage', data_new)
    with open(FILE_NAME, 'r') as in_json:
        data_in = json.load(in_json)
        print('[DEBUG-storage_controller.add_chat_id_to_storage] - data already in storage', data_in)
    data_in[id] = {}
    print('[DEBUG-storage_controller.add_chat_id_to_storage] - data updated to storage', data_in)
    with open(FILE_NAME, 'w') as out_json:
        json.dump(data_in, out_json)
        print('[DEBUG-storage_controller.add_chat_id_to_storage] - data to storage', data_new)

def add_topic_by_id_to_storage(id, topic):
    data_in=read()
    data_in[id][topic]=[]
    print('[DEBUG-storage_controller.add_topic_by_id_to_storage] - data updated to storage', data_in)
    write(data_in)

def add_url_by_id_and_topic_to_storage(id, topic, url):
    data_in=read() 
    data_in[id][topic].append(url)
    print('[DEBUG-storage_controller.add_topic_by_id_to_storage] - data updated to storage', data_in[id][topic])
    write(data_in)


############# LIST
def list_topics_by_id(id):
    data_in=read()
    print('[DEBUG-storage_controller.list_bookmarks_by_id_and_topic] - list ', data_in[id])
    return data_in[id]


def list_bookmarks_by_id_and_topic(id, topic):
    data_in=read()
    print('[DEBUG-storage_controller.list_bookmarks_by_id_and_topic] - list ', data_in[id][topic])
    return data_in[id][topic]


########### REMOVE
def remove_topic_by_id(id, topic):
    data_in=read()
    print('[DEBUG-storage_controller.remove_topic_by_id] - list ', data_in[id])
    res = data_in.pop(topic, None)
    if res != None:
        print('[DEBUG-storage_controller.remove_topic_by_id] - deleted  from storage ', res)
    else:
        print('[DEBUG-storage_controller.remove_topic_by_id] - nothing to delete ')
    return data_in[id]

def remove_url_by_id_and_topic(id, topic, url):
    data_in=read()
    print('[DEBUG-storage_controller.remove_url_by_id_and_topic_] - list ', data_in[id][topic])
    try:
        data_in[id][topic].remove(url)
        print('[DEBUG-storage_controller.remove_url_by_id_and_topic_] - deleted  from storage topic-{}:url-{} '.format(topic, url))
        write(data_in)
    except ValueError as error:
        print("[ERROR] - ELEMNT DOESNOT EXISTS", error)
