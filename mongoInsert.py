import pymongo
import json

'''
数据库中插入数据操作
在json文件中写入待插入数据，读取文件并写入数据库中
'''


def mongodb_insert():
    client = pymongo.MongoClient('mongodb://localhost:27017/')  # 连接到mongoDB
    db_list = client.list_database_names()                      # 获取数据库名
    print("db List: " + str(db_list))                           # 打印数据库名

    db_str = input('db to use:')                                # 输入数据库名
    mydb = client[db_str]                                       # 选中数据库名
    print("collections: " + str(mydb.collection_names()))       # 打印当前数据库的数据表名
    collection_str = input('collection to use:')                # 输入数据表名
    my_collection = mydb[collection_str]                        # 选择待操作的数据表

    file_name = input('file name(format json):')                # 获取数据文件名(.json)
    dict_list = list()                                          # 数据暂存列表

    '''从json数据文件中读取待插入数据并存入暂存列表中'''
    with open(file_name, 'r') as f:
        for line in f:
            temp = json.loads(line)
            dict_list.append(temp)

    '''插入数据操作,每次写入一个，并打印已插入数据的id'''
    for key in dict_list:
        post = key
        post_id = my_collection.insert_one(post).inserted_id
        print(post_id)

mongodb_insert()
