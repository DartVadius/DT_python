import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
import os

RDB_HOST = os.environ.get('RDB_HOST') or 'localhost'
RDB_PORT = os.environ.get('RDB_PORT') or 28015
BOOK_DB = 'book_app'

connection = r.connect(host=RDB_HOST, port=RDB_PORT)
try:
    r.db_create(BOOK_DB).run(connection)
    r.db(BOOK_DB).table_create('addresses').run(connection)
    r.db(BOOK_DB).table_create('notes').run(connection)
    print('Database setup completed.')
except RqlRuntimeError:
    print('App database already exists.')
finally:
    connection.close()
