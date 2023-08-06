# -*- coding: utf-8 -*-
"""
@Author ：Shimon-Cheung
@Date   ：2020/8/14 12:01
@Desc   ：基于dbutils的mysqlmysql工具包
"""
from DBUtils.PooledDB import PooledDB
from loguru import logger
import pymysql
import sys


class MysqlHelper(object):
    """
    基于连接池的工具类，这里又一个约定
    返回值为False的时候，即表示执行语句失败
    返回值为None的时候，表示没有查询到数据
    """

    def __init__(self, **kwargs):
        self.__pool = PooledDB(
            creator=pymysql,  # 使用链接数据库的驱动模块
            maxconnections=20,  # 连接池允许的最大连接数，0和None表示不限制连接数
            mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
            maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
            maxshared=3,  # 链接池中最多共享的链接数量，0和None表示全部共享。
            blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
            setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
            ping=0,  # ping MySQL服务端，检查是否服务可用。0:表示不进行检测
            charset='utf8',  # 指定数据库的编码方式
            **kwargs  # 数据库的连接基本信息
        )
        # 定义一些全局操作对象
        self.__conn = None
        self.__cursor = None
        # 初始化连接对象
        self.__get_db()

    def __get_db(self):
        """
        :return:返回链接对象，游标对象
        """
        self.__conn = self.__pool.connection()
        self.__cursor = self.__conn.cursor(pymysql.cursors.DictCursor)

    def __executor(self, sql, values):
        """
        :param sql: 执行的sql语句
        :param value: 传入的参数
        :return: 全局的游标对象
        """
        try:
            self.__cursor.execute(sql, values)
        except Exception as e:
            logger.error(e)
            self.__get_db()
            try:
                self.__cursor.execute(sql, values)
            except Exception as e:
                logger.error(f"执行语句出错:{e}, sql:{sql}, value:{values}")
                sys.exit(1)

    def find_one(self, sql, values=None):
        """
        :param sql:需要执行的sql语句，字符串类型
        :param values: 需要传入的参数
        :return: 返回一条数据，字典类型
        """
        self.__executor(sql=sql, values=values)
        result = self.__cursor.fetchone()
        return result

    def find_all(self, sql, values=None):
        """
        :param sql:需要执行的sql语句，字符串类型
        :param values: 需要传入的参数
        :return: 返回多条数据，列表类型
        """
        self.__executor(sql=sql, values=values)
        result = self.__cursor.fetchall()
        if len(result) == 0:
            result = None
        return result

    def insert_one(self, sql, values=None):
        """
        :param sql:  需要执行的sql语句，字符串类型
        :param values: 需要传入的参数
        :return: 返回插入的id值
        """
        self.__executor(sql=sql, values=values)
        self.__conn.commit()
        insert_id = self.__cursor.lastrowid
        return insert_id

    def update(self, sql, values=None):
        """
        :param sql:  需要执行的sql语句，字符串类型
        :param values: 需要传入的参数
        :return: 返回更新数据的条数
        """
        self.__executor(sql=sql, values=values)
        self.__conn.commit()
        up_count = self.__cursor.rowcount
        return up_count

    def delete(self, sql, values=None):
        """
        :param sql:  需要执行的sql语句，字符串类型
        :param values: 需要传入的参数
        :return: 返回删除数据的条数
        """
        self.__executor(sql=sql, values=values)
        self.__conn.commit()
        del_count = self.__cursor.rowcount
        return del_count

    def save_db(self, data, data_table, find_dict, duplicate_update=False):
        """
        :param data: 保存的数据
        :param data_table: 需要操作的鼠标表名
        :param find_dict: 唯一索引
        :param duplicate_update: 是否更新
        :return: 执行方式，已经数量
        """
        find_keys = list(find_dict.keys())
        is_find = False
        if find_dict:
            sql = "select count(1) from `" + data_table + "` where " + " and ".join(
                ["`" + i + "`" + "= %s" for i in find_keys])
            item = self.find_one(sql, list(find_dict.values()))
            if item and item['count(1)'] > 0:
                is_find = True
        keys = list(data.keys())
        if not is_find:
            insert_sql = "insert into `" + data_table + "` " + "(" + ",".join(["`" + i + "`" for i in keys]) + \
                         ") values (" + ",".join(["%s" for i in keys]) + ")"
            count_num = self.insert_one(insert_sql, values=list(data.values()))
            print('insert', count_num)
        elif duplicate_update:
            update_sql = "update `" + data_table + "` set " + ", ".join(["`" + i + "`" + "= %s" for i in keys]) \
                         + " where " + " and ".join(["`" + i + "`" + "= %s" for i in find_keys])
            count_num = self.update(update_sql, values=list(data.values()) + list(find_dict.values()))
            print('update', count_num)
        else:
            print('pass', 0)
