import pymongo
from pprint import pprint

def mongodb_search():
    client = pymongo.MongoClient('mongodb://localhost:27017/')  # 连接到mongoDB
    db_list = client.list_database_names()                      # 获取数据库名
    print('db List: ' + str(db_list))                           # 打印数据库名

    db_str = input('db to use:')                            # 输入数据库名
    my_db = client[db_str]                                  # 选中数据库名
    print('collections: ' + str(my_db.collection_names()))  # 打印当前数据库的数据表名
    collection_str = input('collection to use: ')           # 输入数据表名
    my_collection = my_db[collection_str]                   # 选择待操作的数据表

    print('TABLE DATA:')
    for x in my_collection.find():                              # 逐行打印数据表的内容
        pprint(x)

    print('Set search conditions.')
    search_dic = dict()     # 将查询条件放入该字典内
    while True:
        flag = input('0: continue, 1: stop input.')
        if flag == str(1):
            break
        key = input('key:')
        value = input('value:')
        search_dic[key] = value

    x = my_collection.find(search_dic)      # 根据search_dic中的键值对来寻找
    print(x.count(), "documents found.")
    for key in x:       # 打印查找到的文档
        pprint(key)

    pprint('end')

mongodb_search()
