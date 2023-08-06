#   coding: utf-8
#   This file is part of potentialmind.

#   potentialmind is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License.

__author__ = 'Guanjie Wang'
__version__ = 1.0
__maintainer__ = 'Guanjie Wang'
__email__ = "gjwang@buaa.edu.cn"
__date__ = "2020/06/26"

import pymongo
from importlib import import_module


class DancingDb(object):
    def __init__(self, host, port, databasename, username, userpassword, admin_name=None, admin_pwd=None):

        self.c = {}
        self.c['host'] = host
        self.c['port'] = port
        self.c['databasename'] = databasename
        self.c['username'] = username
        self.c['userpassword'] = userpassword
        self.c['admin_name'] = admin_name
        self.c['admin_pwd'] = admin_pwd

    @classmethod
    def from_dict(cls, d: dict):
        d = {}
        d['host'] = '115.25.160.11'
        d['port'] = int(57107)
        d['databasename'] = 'ttttt1'
        d['username'] = 'gjwang'
        d['userpassword'] = '123abc'
        d['admin_name'] = 'admin'
        d['admin_pwd'] = 'admin'
        return cls(**d)

    @property
    def host(self):
        return self.c['host']

    @property
    def port(self):
        return self.c['port']

    @property
    def databasename(self):
        return self.c['databasename']

    @property
    def username(self):
        return self.c['username']

    @property
    def password(self):
        return self.c['userpassword']

    @property
    def client(self):
        return pymongo.MongoClient("mongodb://%s:%s" % (self.host, self.port))

    def __connect_admin(self):
        # return self.connect('admin',
        #                     self.c.get('admin_name', 'admin'),
        #                     self.c.get('admin_pwd', 'admin'))
        myclient = self.client
        db = myclient['admin']
        db.authenticate(self.c.get('admin_name', 'admin'), self.c.get('admin_pwd', 'admin'))
        return myclient

    @property
    def all_databases(self):
        return self.__connect_admin().list_database_names()

    @property
    def all_collection_names(self):
        return self.connect_db().list_collection_names()

    def connect_db(self):
        return self.connect(self.databasename, self.username, self.password)

    def connect(self, databasename, username, password):
        myclient = self.client
        db = myclient[databasename]
        db.authenticate(username, password)
        return db

    def __getitem__(self, item):
        return self.connect_db()[item]

    def _create_db(self, db_name, user_name, user_pwd):
        mydb = self.__connect_admin()[db_name]
        mydb.add_user(user_name, user_pwd,
                      roles=[{"role": "dbAdmin", 'db': db_name},
                             {"role": 'readWrite', 'db': db_name}])
        mydb.authenticate(user_name, user_pwd)
        return mydb

    def _create_dbadmin_user(self, db_name, user_name, user_pwd):
        a = self.__connect_admin().list_database_names()
        if db_name not in a:
            mydb = self._create_db(db_name=db_name,
                                  user_name=user_name,
                                  user_pwd=user_pwd)

            self.__insert_initial_info(mydb)
            return True
        else:
            return False

    def init(self):
        is_create = self._create_dbadmin_user(self.databasename, self.username, self.password)
        if not is_create:
            print('Initial no empty database')
            self.__connect_admin().drop_database(self.databasename)
            self._create_dbadmin_user(self.databasename, self.username, self.password)
        print("Initial successfully!")

    @staticmethod
    def __insert_initial_info(mydb):
        mycollec = mydb['dancingcell']
        test_dict = {'DancingCell': import_module('dancingcell').__version__,
                     'Author': 'ALKEMIE(Artificial Learning and Knowledge Enhanced Materials '
                               'Informatics Engineering)'}
        mycollec.insert_one(test_dict)

