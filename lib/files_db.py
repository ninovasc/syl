"""Uses sqlite3 library to manage files send on each chat group"""
import sqlite3
import sys

class Files_DB(object):

    def create(self, _db_name="server"):
        #db_exists = os.path.exists(_db_name)
        try:
            conn = sqlite3.connect(_db_name + ".sqlite")
            drop = '''DROP TABLE IF EXISTS files;'''
            conn.execute(drop)
            create = '''create table files(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            FILE LONGTEXT,
            FILE_NAME TEXT,
            GROUPS TEXT);'''
            conn.execute(create)
            conn.close()
            return True
        except:
            print "Unexpected error:", sys.exc_info()[0]
            return False

    def insert_file(self, _group, _file_name, _file_binary, _db_name="server"):
        try:
            conn = sqlite3.connect(_db_name + ".sqlite")
            sql = '''INSERT INTO files
            (FILE, FILE_NAME, GROUPS)
            VALUES(?, ?, ?);'''
            conn.execute(
                sql,
                [_file_binary, _file_name, _group]
            )
            conn.commit()
            conn.close()
            return True
        except:
            print "Unexpected error:", sys.exc_info()[0]
            return False

    def file_names_by_group(self, _group, _db_name="server"):
        try:
            conn = sqlite3.connect(_db_name + ".sqlite")
            conn.row_factory = dict_factory
            cur = conn.cursor()
            sql = '''SELECT FILE_NAME FROM files
                WHERE GROUPS = :group;'''
            param = {"group" : _group}
            cur.execute(sql, param)
            files_list = cur.fetchall()
            conn.close()
            return files_list
        except:
            print "Unexpected error:", sys.exc_info()[0]
            return False

    def file_by_name_group(self, _file_name, _group, _db_name="server"):
        try:
            conn = sqlite3.connect(_db_name + ".sqlite")
            conn.row_factory = dict_factory
            cur = conn.cursor()
            sql = '''SELECT FILE FROM files
                WHERE FILE_NAME = :file_name AND GROUPS = :groups;'''
            param = {"file_name" : _file_name, "groups" : _group}
            cur.execute(sql, param)
            b64file = cur.fetchone()["FILE"]
            conn.close()
            return b64file
        except:
            print "Unexpected error:", sys.exc_info()[0]
            return False

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
