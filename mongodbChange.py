#updateStatement format: {'$set':{key:value}}

import pymongo
from pprint import pprint

'''
数据库修改操作：修改数据
'''
def mongodb_change():
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

    '''输入需要修改的数据键值对,格式为： key:value'''
    print('Set the condition:')
    condition_dic = dict()
    while True:     # 如果是空字典，那么返回全部文档
        flag = input('0: continue, 1: stop input.')
        if flag == str(1):
            break
        key = input('key:')
        value = input('value:')
        condition_dic[key] = value

    myquery = condition_dic                 # 查询条件：键值对字典{key:value}

    my_doc = my_collection.find(myquery)    # 查询操作，将包含键值对{key:value}的数据存储到my_doc中

    print('Documents found:')
    for key in my_doc:
        pprint(key)                     # 打印查询的所有结果

    print('Modify Document:')
    '''记录需要修改的键值对为update_dic'''
    update_dic = dict()
    while True:
        flag = input('0 to contintue, 1 to stop.')
        if flag == str(1):
            break
        '''输入需要修改的数据的键'''
        update_key = input('key to update(if not exist, create a new key:value):')
        '''输入需要修改的数据的值'''
        update_value = input('value to update:')
        '''直接复制操作,修改以后的键值为 {update_key:update_value}'''
        update_dic[update_key] = update_value

    '''创建待修改的字段'''
    update_statement = dict()
    update_statement['$set'] = update_dic

    '''
    update_many() 方法修改文档中的记录。该方法第一个参数为查询的条件，第二个参数为要修改的字段
    修改字段的格式为updateStatement format: {'$set':{key:value}}
    更新操作,将数据表的第一个符合myquery查询条件的数据的指定键值对修改为update_statement
    '''
    if len(update_statement) != 0:
        x = my_collection.update_many(myquery, update_statement)
        print(x.modified_count, "documents update.")

mongodb_change()
