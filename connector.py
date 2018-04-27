import os
import rethinkdb as r


def connect_decorator(method_to_decorate):
    def connect_wrapper(self, *args):
        self.connection = r.connect(host=self.RDB_HOST, port=self.RDB_PORT, db=self.BOOK_DB)
        value = method_to_decorate(self, *args)
        self.connection.close()
        return value
    return connect_wrapper


class Connector:
    RDB_HOST = os.environ.get('RDB_HOST') or 'localhost'
    RDB_PORT = os.environ.get('RDB_PORT') or 28015
    BOOK_DB = 'book_app'
    connection = None

    @connect_decorator
    def get_by_id(self, table_name, row_id):
        value = r.table(table_name).get(row_id).run(self.connection)
        return value

    @connect_decorator
    def get_all(self, table_name):
        value = r.table(table_name).order_by('second_name').run(self.connection)
        return value
