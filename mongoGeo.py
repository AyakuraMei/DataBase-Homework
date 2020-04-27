import pymongo
import json
import pprint
import requests
import pymongo.helpers


class mongo_geo(object):
    client = 0                  # 客户端名
    my_collection = 0           # 数据库表/集合
    data_arr = []               # 数据暂存列表
    def __init__(self, clientname):
        self.client = pymongo.MongoClient(clientname)               # 连接到mongoDB
        print("db List:" + str(self.client.list_database_names()))  # 获取并打印数据库名
        db_name = input("db to use:")                               # 输入数据库名
        mydb = self.client[db_name]                                 # 选中数据库名
        print("Collection List:" + str(mydb.collection_names()))    # 打印当前数据库的数据表名
        collection_use = input("Collection to use:")                # 选择需要使用的collection
        self.my_collection = mydb[collection_use]                   # 选择待操作的数据表


    ''' 
    文件写入测试函数
    在test.json写入一组数据 {'x':'3', 'y':'4', 'loc':{'x': 1,'y': 2}}
    '''
    def writejson(self):    #test case
        data = {'x':'3', 'y':'4', 'loc':{'x': 1,'y': 2}}
        json_str = json.dumps(data)         # json.dumps()用于将字典形式的数据转化为字符串
        with open('test.json', 'a') as f:
            f.write(json_str)               # 将data写入文件
            f.write('\n')


    '''  
    读取文件函数
    从指定json文件中读取单行数据解析为字典,加入数据暂存列表data_arr中
    '''
    def readfile(self):
        #读取json文件
        file_name = input('file name(format json):')
        #解析,json格式
        with open(file_name, 'r') as f:
            for line in f:
                temp = json.loads(line)                 # json.loads()用于将字符串形式的数据转化为字典
                self.data_arr.append(temp)              # 将解析好的json（单独一行）加入到data_arr中
        if len(self.data_arr) != 0:                     # 如果添加后，data_arr的长度不为0，则表明读取成功
            print('ADD DATA SUCCESS.')
        else:
            print('EMPTY.')                             # 否则提示文件内容为空


    '''
    写入文件函数
    将数据从数据暂存列表data_arr中按行为单位写入数据库/表中
    '''
    def writedata(self):
        if len(self.data_arr) == 0:                         # 数据为空,则提示empty
            print('data is empty.')
        else:
            # for key in self.data_arr:                     # 将数据逐个从数据暂存列表中写入数据库/表
            #     post = key
            #     self.my_collection.insert_one(post)
            self.my_collection.insert_many(self.data_arr)   # 将数据一次性从数据暂存列表中写入数据库/表

    '''
    清除数据暂存列表函数
    清除self.data_arr列表
    '''
    def dataclear(self):    #清除date中的数据
        return self.data_arr.clear()

    '''
    读取文件操作
    执行readfile()函数,获取json文件的数据并存储到self.data_arr列表
    '''
    def dataappend(self):
        return self.readfile()


    '''
    pprint 包含一个“美观打印机”，用于生成数据结构的一个美观视图。
    格式化工具会生成数据结构的一些表示，不仅可以由解释器正确地解析，而且便于人类阅读。
    输出尽可能放在一行上，分解为多行时则需要缩进。
    '''
    def pprint(self):
        pprint.pprint(self.data_arr)


    '''
    
    通过requests和外部接口获得以经度纬度为基础的坐标    longitude:经度;latitude:纬度
    需要联网使用
    经过处理后获得的store file可以配合culcluategeonear来计算相对应的距离
    '''
    def make_pos(self):

        file_name = 'locationTest.json'
        file = open(file_name, 'w')

        return_list = list()

        # 设置longitude(经度)范围
        longitude_begin = input('longitude begin:')
        longitude_end = input('longitude end:')
        longitude = list()
        longitude.append(longitude_begin)
        longitude.append(longitude_end)
        # 设置latitude(纬度)范围
        latitude_begin = input('latitude begin:')
        latitude_end = input('latitude end:')
        latitude = list()
        latitude.append(latitude_begin)
        latitude.append(latitude_end)

        gap = input('gap:')         # 间隔(精度)

        # 设置经度纬度起始值
        loop_i = float(longitude[0])
        loop_k = float(latitude[0])

        # 经纬度列表
        longitude_list = list()
        latitude_list = list()

        # 每隔一个间隔gap加入一个经纬度值
        while loop_i <= float(longitude[1]):
            longitude_list.append(loop_i)
            loop_i = loop_i + float(gap)
        while loop_k <= float(latitude[1]):
            latitude_list.append(loop_k)
            loop_k = loop_k + float(gap)

        ''''
        每对经纬值获取一个地图网页的数据,并写入return_list中
        需要联网
        返回的文件可以在locationTest.json中查看
        共获取key*key_1个网页
        每个网页为一个区域的地点集合数据
        '''
        for key in longitude_list:
            for key_1 in latitude_list:
                url = 'http://ditu.amap.com/service/regeo?longitude=' + str(key) + \
                    '&latitude=' + str(key_1)
                r = requests.get(url)
                return_list.append(r)

        '''将网页数据转化为json格式打印并按行写入文件中'''
        for key in return_list:
            json_data = json.dumps(key.json())
            # pprint.pprint(json_data)
            file.write(json_data + '\n')
        file.close()


        store_file = input('store file name(*.json):')

        file_1 = open(store_file, 'w')
        locate = dict()                 # 用字典存储地点
        pos = list()                    # 位置列表，存储经纬度，format: [latitude, longtitude]

        '''
        对文件样式进行转化
        将locationTest.json文件中的网页数据转化为地图数据
        '''
        with open('locationTest.json', 'r') as f:
            '''单行数据为一个网页的数据'''
            for line in f:
                test_string = line
                # print(test_string)
                string = json.loads(test_string)
                #pprint.pprint(string)
                try:
                    '''每个网页解析存储一个区域的一组地点'''
                    for key in string['data']['poi_list']:  #对于poi_list中的每个对象
                        pos.append(float(key['latitude']))
                        pos.append(float(key['longitude']))
                        locate['desc'] = key['name']
                        locate['xy'] = pos
                        print(locate)
                        json_str = json.dumps(locate)
                        locate.clear()
                        pos.clear()
                        file_1.write(json_str + '\n')

                    '''如果发生KeyError, 通常为不存在 'poi_list' 键'''
                except KeyError:
                    continue


    '''创建2d索引'''
    def create_2d_index(self, loc):
        self.my_collection.create_index([(loc, pymongo.GEO2D)])
        self.my_collection.ensure_index([(loc, pymongo.GEO2D)])


    def culculategeonear(self):

        '''使用聚集函数来计算距离'''
        location_x = input('pos x:')
        location_y = input('pos y:')

        '''存放计算的起始坐标'''
        location_arr = []
        location_arr.append(float(location_x))
        location_arr.append(float(location_y))

        '''
        使用聚集函数计算距离
        需要数据库设置2d索引
        输出结果包含数据表内的地点名desc、地点坐标xy和每个地点到该输入的坐标的距离distance，且距离从小到大排序
        '''
        print('List:')
        try:
            # 聚集函数的管道
            # $geoNear设置管道为输出接近某一地理位置的有序文档
            # distanceField 存储计算得到的距离
            pipeline = [{'$geoNear': {'near': location_arr, 'distanceField': 'distance'}}]
            for x in self.my_collection.aggregate(pipeline):    # 打印获得的文档和对应的距离
                print(x)
        except pymongo.helpers.OperationFailure:    # 如果这个数据库的collection没有设置2dsphere，那么创建2dsphere
            print('NO 2dsphere, creating 2dsphere...')
            self.create_2d_index('xy')
        finally:
            pipeline = [{'$geoNear': {'near': location_arr, 'distanceField': 'distance'}}]
            for x in self.my_collection.aggregate(pipeline):
                print(x)
