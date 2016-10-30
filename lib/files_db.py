"""
Uses sqlite3 library to manage files send on each chat group.
"""
import sqlite3
import sys

class Files_DB(object):
    """
    @brief      Class for files db.
    """

    def create(self, _db_name="server"):
        """
        @brief      Create a database, if already exist data from another
                    old server it's excluded.

        @param      self      The object
        @param      _db_name  The database name

        @return     return True if success.
        """
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

    def insert_file(self, _group, _file_name, _file, _db_name="server"):
        """
        @brief      Insert a file in database, the file is a Base 64 encoded
                    text.

        @param      self          The object
        @param      _group        The group
        @param      _file_name    The file name
        @param      _file         The file
        @param      _db_name      The database name

        @return     Return True if file was inserted on database
        """
        try:
            conn = sqlite3.connect(_db_name + ".sqlite")
            sql = '''INSERT INTO files
            (FILE, FILE_NAME, GROUPS)
            VALUES(?, ?, ?);'''
            conn.execute(
                sql,
                [_file, _file_name, _group]
            )
            conn.commit()
            conn.close()
            return True
        except:
            print "Unexpected error:", sys.exc_info()[0]
            return False

    def file_names_by_group(self, _group, _db_name="server"):
        """
        @brief      List files stored in a group

        @param      self      The object
        @param      _group    The group
        @param      _db_name  The database name

        @return     Return a list of dictionaries with file names.
        """
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
        """
        @brief      Find file by name and group, this is a key for a file.

        @param      self        The object
        @param      _file_name  The file name
        @param      _group      The group
        @param      _db_name    The database name

        @return     return a Base 64 file.
        """
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

    def delete_files_by_group(self, _group, _db_name="server"):
        """
        @brief      delete files stored in a group

        @param      self      The object
        @param      _group    The group
        @param      _db_name  The database name

        @return     Return True if files was deleted
        """
        try:
            conn = sqlite3.connect(_db_name + ".sqlite")
            cur = conn.cursor()
            sql = '''DELETE FROM files
                WHERE GROUPS = :group;'''
            param = {"group" : _group}
            cur.execute(sql, param)
            conn.close()
            return True
        except:
            print "Unexpected error:", sys.exc_info()[0]
            return False


def dict_factory(cursor, row):
    """
    @brief      Create a fatory to convert result of a query in a dictionary.
                This is used in 'file_names_by_group', using row_factory
                attribute from a connection of sqlite3

    @param      cursor  The cursor
    @param      row     The row

    @return     Return a dictionary from a query.
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
