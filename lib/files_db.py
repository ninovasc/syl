import sqlite3
import os.path

class Files_DB(object):

    def __init__(self, _db_name):
        self.conn=sqlite3.connect(_db_name + ".sqlite")

    #def open(self, _db_name):
    #    self.conn = sqlite3.connect(_db_name + ".sqlite")

    def create(self, _db_name):
        #db_exists = os.path.exists(_db_name)
        self.conn = sqlite3.connect(_db_name + ".sqlite")
        drop = '''DROP TABLE IF EXISTS files;'''
        self.conn.execute(drop)
        create = '''create table files(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        FILE BLOB,
        FILE_NAME TEXT,
        GROUPS TEXT);'''
        self.conn.execute(create)

    def insert_file(self, _group, _file_name, _file_binary):
        sql = '''INSERT INTO files
        (FILE, FILE_NAME, GROUPS)
        VALUES(?, ?, ?);'''
        self.conn.execute(
            sql,
            [sqlite3.Binary(_file_binary), _file_name, _group]
        )
        self.conn.commit()

    def file_names_by_group(self, _group):
        sql = '''SELECT FILE_NAME FROM files
            WHERE GROUPS = :group;'''
        param = {"group" : _group}
        return self.conn.execute(sql, param)

    def file_by_name_group(self, _file_name, _group):
        sql = '''SELECT FILE FROM files
            WHERE FILE_NAME = :file_name AND GROUPS = :group;'''
        param = {"file_name" : _file_name, "group" : _group}
        return self.conn.execute(sql, param)
