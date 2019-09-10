"""
说明：创建对数据库操作的封装类，在数据库中存储了一个表，标的内容如下：
+----+-------+--------+----------+------+
| id | owner | sender | key_word | type |
+----+-------+--------+----------+------+
这个类封装了连接数据库、查看表中所有数据、增加一条过滤规则、删除一条过滤规则、查找一个用户所有的过滤规则和清空表的操作
作者：71117205丁婧伊
创建时间：2019/8/28
最后一次修改时间：2019/8/29
"""
import pymysql
import json


# 数据库操作的封装类，封装了连接数据库、查看表中所有数据、增加一条过滤规则、删除一条过滤规则、查找一个用户所有的过滤规则和清空表的操作
class Filter_operation:

    def conn(self, host="127.0.0.1", user="root", password="Heyingzhi666@", database="spamServer"):
        """
        连接数据库函数
        :param host: 主机号
        :param user: 用户
        :param password: 密码
        :param database: 数据库
        :return: 返回连接成功的数据库
        """
        db = pymysql.connect(host, user, password, database)
        return db

    def find_all_owner(self):
        """
        查看表中所有的数据函数, 用于服务器端对数据库中的数据进行管理
        :return: 返回表中所有数据的列表，方便服务器端查看
        """
        # 创建列表
        server_list = []
        # 连接数据库
        db = self.conn()
        cursor = db.cursor()
        sql = "select * from filter_rule"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            # 读取sql语句返回的数据
            for row in results:
                id = row[0]
                owner = row[1]
                sender = row[2]
                keyword = row[3]
                type = row[4]
                # 创建字典对象
                rule_dir = {'id': id, 'owner': owner, 'sender': sender, 'key_word': keyword, 'type': type}
                # 加入列表
                server_list.append(rule_dir)
        except Exception as e:
            print("查看所有数据时发生错误！", e)
        # 关闭数据库
        db.close()
        return server_list

    def add_one_rule(self, client_dict):
        """
        增加一条过滤规则，从客户端传入一条字典数据,服务器返回一条字典表示操作结果，返回1代表正确，-1代表不正确
        :param client_dict: 字典类型的过滤规则，格式如下：
        {'action':'post', 'content':[{'id':'','owner':'','sender':'','key_word':'','type':''}]}
        :return: 字典类型的返回结果，格式如下：
        {'action': 'response-post', 'content': 1}
        """
        # 读取字典对象中的数据
        owner = client_dict['content'][0]['owner']
        sender = client_dict['content'][0]['sender']
        key_word = client_dict['content'][0]['key_word']
        type = client_dict['content'][0]['type']
        # 返回结果中，result=1操作成功，result=-1操作失败
        result = 1
        # 连接数据库
        db = self.conn()
        cursor = db.cursor()
        sql = "insert into filter_rule(owner, sender, key_word, type) values('%s', '%s', '%s', '%s')" \
              % (owner, sender, key_word, type)
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            print("添加时发生错误，回滚", e)
            db.rollback()
            result = -1
        # 关闭数据库
        db.close()
        # 创建字典对象，result=1操作成功，result=-1操作失败
        server_dir = {'action': 'response-post', 'content': result}
        return server_dir

    def delete_one_rule(self, client_dict):
        """
        删除一条规则，如果表中有多条相同的规则则全部都删去
        客户端发送一条仅包含一条规则的json数据，服务器返回一条json数据表示操作结果
        :param client_dict: 字典对象
        :return: 字典对象
        """
        # 读取字典对象中的数据
        owner = client_dict['content'][0]['owner']
        sender = client_dict['content'][0]['sender']
        key_word = client_dict['content'][0]['key_word']
        type = client_dict['content'][0]['type']
        # 返回结果中，result=1操作成功，result=-1操作失败
        result = 1
        # 连接数据库
        db = self.conn()
        cursor = db.cursor()
        sql = "delete from filter_rule where owner = '%s' and sender = '%s' and key_word = '%s' and type = '%s'" % (
        owner, sender, key_word, type)
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            print("删除时发生错误，回滚", e)
            result = -1
        # 关闭数据库
        db.close()
        # 创建字典对象，result=1操作成功，result=-1操作失败
        server_dir = {'action': 'response-post', 'content': result}
        return server_dir

    def search_owner(self, client_dict):
        """
        查找一个用户的所有过滤规则,客户端传递字典数据，读取其中的owner进行查询，服务器返回一个字典表示结果
        :param client_dict:
        :return:
        """
        # 读取字典对象中的数据
        owner = client_dict['content']
        # 创建列表
        server_list = []
        # 连接数据库
        db = self.conn()
        cursor = db.cursor()
        sql = "select id, owner, sender, key_word, type from filter_rule where owner = '%s'" % (owner)
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                id = row[0]
                owner = row[1]
                sender = row[2]
                keyword = row[3]
                type = row[4]
                # 创建字典对象
                rule_dir = {'id': id, 'owner': owner, 'sender': sender, 'key_word': keyword, 'type': type}
                # 加入列表
                server_list.append(rule_dir)
            db.commit()
        except Exception as e:
            print("查找时发生错误，回滚", e)
        # 关闭数据库
        db.close()
        # 创造字典对象
        server_dict = {'action': 'response-info', 'content': server_list}
        return server_dict

    def clean_table(self):
        """
        清空表
        :return:
        """
        result = True
        # 连接数据库
        db = self.conn()
        cursor = db.cursor()
        sql = "delete from filter_rule"
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            print("清空所有数据时发生错误，回滚", e)
            result = False
        # 关闭数据库
        db.close()
        return result
