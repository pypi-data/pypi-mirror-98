"""
操作mysql、oracle数据库
"""
import pymysql
import cx_Oracle


class MysqlDb(object):
    """
    Mysql操作类
    """

    def __init__(self, db):
        self.host = db["host"]
        self.user = db["user"]
        self.password = db["password"]
        self.database = db["database"]
        self.port = db["port"]
        self.connect_timeout = 5
        self.max_allowed_packet = 16 * 1024 * 1024
        self.read_timeout = 10
        self.write_timeout = 10

    def db_connect(self):
        """
        连接数据库
        """
        count, conn, cur = 1, None, None
        while True:
            try:
                conn = pymysql.connect(
                    self.host,
                    self.user,
                    self.password,
                    self.database,
                    self.port,
                    connect_timeout=self.connect_timeout,
                    max_allowed_packet=self.max_allowed_packet,
                    read_timeout=self.read_timeout,
                    write_timeout=self.write_timeout,
                    charset="utf8",
                )
                cur = conn.cursor()
                break
            except Exception as e:
                if count == 3:
                    raise Exception(e)
                count += 1
        return conn, cur

    def db_close(self, conn, cur):
        """
        关闭数据库
        """
        if conn and cur:
            cur.close()
            conn.close()

    def sql_execute(self, sql, param=None):
        """
        执行sql
        :param sql: UPDATE语句, DELETE语句, INSERT语句
        :param sql: "INSERT INTO table name (field1, field2) VALUES(%s, %s)"
        :param param: 一元元组 (1, 1)
        :return last_id: INSERT语句返回自增ID
        """
        result = 0
        conn, cur = self.db_connect()
        try:
            if conn and cur:
                # 返回影响的行数
                result = cur.execute(sql, param)
                conn.commit()
                # 提交之后，获取刚插入的数据自增的ID
                if cur.lastrowid:
                    result = cur.lastrowid
        except Exception as e:
            conn.rollback()
            raise Exception(e)
        finally:
            self.db_close(conn, cur)
        return result

    def sql_select(self, sql, param=None):
        """
        SQL查询
        :param sql: SELECT语句
        :param param: 一元元组 (1, 1)
        :return result: 返回字段名和数据, data是二元元组
        """
        result = {"field": [], "data": []}
        conn, cur = self.db_connect()
        try:
            if conn and cur:
                cur.execute(sql, param)
                result["field"] = [field[0] for field in cur.description]
                result["data"] = cur.fetchall()
                conn.commit()
        except Exception as e:
            conn.rollback()
            raise Exception(e)
        finally:
            self.db_close(conn, cur)
        return result

    def many_insert(self, sql, param=None):
        """
        批量插入
        :param sql: "INSERT INTO table name (field1, field2) VALUES(%s, %s)"
        :param param: 二元元组 ((1, 1), (2, 2))
        """
        conn, cur = self.db_connect()
        try:
            if conn and cur:
                cur.executemany(sql, param)
                conn.commit()
        except Exception as e:
            conn.rollback()
            raise Exception(e)
        finally:
            self.db_close(conn, cur)

    def many_execute(self, transactions):
        """
        批量执行，提交事务
        :param transactions 数组字典 [{"sql": "", "param": (1, 2)}, {"sql": "", "param": None}]
        """
        conn, cur = self.db_connect()
        try:
            if conn and cur:
                for transaction in transactions:
                    cur.execute(transaction["sql"], transaction.get("param"))
                conn.commit()
        except Exception as e:
            conn.rollback()
            raise Exception(e)
        finally:
            self.db_close(conn, cur)


class OracleDb(object):
    """
        cx_Oracle操作类
    """

    def __init__(self, db):
        self.host = db["host"]
        self.user = db["user"]
        self.password = db["password"]
        self.database = db["database"]
        self.port = db["port"]

    def db_connect(self):
        """
        连接数据库
        """
        count, conn, cur = 1, None, None
        while True:
            try:
                conn = cx_Oracle.connect(
                    "{user}/{password}@{host}:{port}/{db}".format(
                        user=self.user,
                        password=self.password,
                        host=self.host,
                        port=str(self.port),
                        db=self.database,
                    )
                )
                cur = conn.cursor()
                break
            except Exception as e:
                if count == 3:
                    raise Exception(e)
                count += 1
        return conn, cur

    def db_close(self, conn, cur):
        """
        关闭数据库
        """
        if conn and cur:
            cur.close()
            conn.close()

    def sql_select(self, sql, param=None):
        """
        SQL查询
        :param sql: SELECT语句
        :param param: dict
        :return result: 返回字段名和数据
        """
        if param is None:
            param = {}

        result = {"field": [], "data": []}
        conn, cur = self.db_connect()
        try:
            if conn and cur:
                cur.execute(sql.strip(";"), **param)
                result["field"] = [field[0] for field in cur.description]
                result["data"] = cur.fetchall()
                # 查询LOB
                if result["data"] and isinstance(result["data"][0][0], cx_Oracle.LOB):
                    result["data"] = [[result["data"][0][0].read()]]
                conn.commit()
        except Exception as e:
            conn.rollback()
            raise Exception(e)
        finally:
            self.db_close(conn, cur)
        return result
