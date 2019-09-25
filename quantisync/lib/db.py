import os

from peewee import SqliteDatabase, Model, DatabaseProxy

from quantisync.config import storage

dbProxy = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = dbProxy


database = SqliteDatabase(storage.DB_PATH)

env = os.environ.get("PYTHON_ENV")

if env == 'test':
    database = SqliteDatabase(storage.DB_TEST_PATH)

dbProxy.initialize(database)
