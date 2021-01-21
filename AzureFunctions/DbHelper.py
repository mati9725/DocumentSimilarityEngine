# -*- coding: utf-8 -*-

import json
import urllib
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
import os.path
import os

class DbHelper:
    
    def __init__(self):
        self.db_config = self.__get_db_config()
        self.engine, classes = self.__get_db()
        self.app_config = classes.app_config
        self.wiki_data = classes.wiki_data
    
    def __get_db_config(self):
        filename = "db.config.json"
        if os.path.isfile(filename):
            with open(filename) as f:
                return json.load(f)
        else:
            config = dict()
            config['db_name'] = os.environ['db.db_name']
            config['server'] = os.environ['db.server']
            config['username'] = os.environ['db.username']
            config['password'] = os.environ['db.password']
            config['scrapper_name'] = os.environ['db.scrapper_name']
            return config
    
    # On mac, run these first:
    # - brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
    # - brew update
    # - brew install msodbcsql17 mssql-tools
    #
    # Install requirements:
    # - pip install pyodbc sqlalchemny
    def __get_db(self):
        database = self.db_config['db_name']
        server = self.db_config['server']
        username = self.db_config['username']
        password = self.db_config['password']
        driver = '{ODBC Driver 17 for SQL Server}'
        
        odbc_str = 'DRIVER='+driver+';SERVER='+server+';PORT=1433;UID='+username+';DATABASE='+ database + ';PWD='+ password
        connect_str = 'mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote_plus(odbc_str)
        
        engine = create_engine(connect_str)
        
        base = automap_base()
        base.prepare(engine, reflect=True)
        return engine, base.classes
    
