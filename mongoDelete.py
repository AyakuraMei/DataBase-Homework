import pymongo
import json
from pprint import pprint

def mongodb_delete():
    client = pymongo.MongoClient('mongodb://localhost:27017/')  # 连接到mongoDB
    db_list = client.list_database_names()                      # 获取数据库名
    print('db List: ' + str(db_list))                           # 打印数据库名

    db_str = input('db to use:')                            # 输入数据库名
    my_db = client[db_str]                                  # 选中数据库名
    print('collections: ' + str(my_db.collection_names()))  # 打印当前数据库的数据表名
    collection_str = input('collection to use: ')           # 输入数据表名
    my_collection = my_db[collection_str]                   # 选择待操作的数据表

    '''打印数据表内容'''
    print('TABLE DATA:')
    for x in my_collection.find():
        pprint(x)

    '''
    delete_conditions_dic为删除操作的查询对象
    '''
    print('Set the condition:')
    flag = 0
    delete_conditions_dic = dict()
    while True:
        flag = input('0: continue, 1: stop input.')
        if flag == str(1):
            break
        key = input('key:')
        value = input('value:')
        delete_conditions_dic[key] = value

    '''
    删除数据操作
    delete_one() 方法来删除文档，该方法第一个参数为查询对象，指定要删除哪些数据。
    '''
    if len(delete_conditions_dic) != 0:
        x = my_collection.delete_many(delete_conditions_dic)
        print(x.deleted_count, "documents deleted.")

mongodb_delete()