import json

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


def read_by_chat_id(id):
    with open(FILE_NAME, 'r') as infile:
        data = json.load(infile)
    return data[id]


def write(data):
    with open(FILE_NAME, 'a') as outfile:
        json.dump(data, outfile)


