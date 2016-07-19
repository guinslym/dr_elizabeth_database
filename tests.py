''' An example of how to mock the sqlite3.connection method '''
''' this is not the test for the sqlalchemy_insert.py file '''

from unittest.mock import MagicMock,Mock
import unittest
import sqlalchemy
import sqlite3
from datetime import datetime
from dateutil.parser import parse

import os
from os import listdir
from os.path import isfile, join

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from sqlite_ex import Tweet, Base, User, Picture, Mention
from sqlite_ex import Hashtag, Url, create_table, Profile

class MyTests(unittest.TestCase):

    def test_sqlite3_connect_success(self):

        sqlite3.connect = MagicMock(return_value='connection succeeded')

        dbc = DataBaseClass()
        sqlite3.connect.assert_called_with('test_database')
        self.assertEqual(dbc.connection,'connection succeeded')


    def test_sqlite3_connect_fail(self):

        sqlite3.connect = MagicMock(return_value='connection failed')

        dbc = DataBaseClass()
        sqlite3.connect.assert_called_with('test_database')
        self.assertEqual(dbc.connection, 'connection failed')

    def test_sqlite3_connect_with_sideaffect(self):

        self._setup_mock_sqlite3_connect()

        dbc = DataBaseClass('good_connection_string')
        self.assertTrue(dbc.connection)
        sqlite3.connect.assert_called_with('good_connection_string')

        dbc = DataBaseClass('bad_connection_string')
        self.assertFalse(dbc.connection)
        sqlite3.connect.assert_called_with('bad_connection_string')

    def _setup_mock_sqlite3_connect(self):

        values = {'good_connection_string':True,
                  'bad_connection_string':False}

        def side_effect(arg):
            return values[arg]

        sqlite3.connect = Mock(side_effect=side_effect)


class DataBaseClass():

    def __init__(self,connection_string='test_database'):
        self.connection = sqlite3.connect(connection_string)


class DrElizabethProject(unittest.TestCase):
    """
    """


    def setUp(self):
        create_table('test_db.db')


    def tearDown(self):
        try:
            os.remove("test_db.db")
        except:
            pass

    def test_datetime(self):
        this_date = {"created_at": "Wed May 04 21:45:09 +0000 2016"}
        created_at = parse(this_date.get('created_at'))
        assert str(created_at.year) == this_date.get('created_at').split()[-1]

    def test_file(self):
        from sqlalchemy_insert import get_the_json_value
        import json
        assert 1 == True
