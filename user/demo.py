# import pymysql
import os

# with open('./sql数据/区县.txt','r',encoding='utf-8')as f:
#     data = f.read()
#     data2 = data.split(';')
#     # print(len(data2))
#     for i in data2[3000:]:
#         # print(i)
#         db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='obj01')
#         cursor = db.cursor()
#         sql=i
#         print(sql)
        # if cursor.execute(sql):
        #     print('successful')
        #     db.commit() #执行数据插入
        # db.close()

for file in os.listdir('../media/media/'):   #上一个文件夹下所有文件夹目录
    print(file)