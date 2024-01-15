import MySQLdb


class Database:
    def __init__(self, db):
        try:
            self.connection = MySQLdb.connect(
                host=db['host'],
                port=db['port'],
                user=db['username'],
                passwd=db['password'],
                db=db["database"],
                charset='utf8',
                use_unicode=True
            )
            self.connection.ping(True)
            self.connection.autocommit(True)
            self.cursor = self.connection.cursor()
            self.connection.show_warnings()
        except Exception as e:
            print(f"{e}")
            raise Exception('ERROR DATABASE:: Mysql is not connected!')

    # @Combinatorics.count
    def query(self, query, show=False):
        try:
            if show:
                return query
            else:
                self.connection.ping(True)
                self.cursor.execute(query)
                count = self.cursor.rowcount
                return count
        except Exception as e:
            print(
                "MYSQL_EXCEPTION:\n{0}\nQuery:\n{1}".format(e, query.strip())
            )
            self.connection.rollback()

    # @Combinatorics.count
    def select(self, query, selectOnce=True, show=False):
        try:
            if show:
                return query
            else:
                self.connection.ping(True)
                cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute(query)

                if selectOnce:
                    return cursor.fetchone()
                else:
                    return cursor.fetchall()

        except Exception as e:
            print(
                "MYSQL_EXCEPTION:\n{0}\nQuery:\n{1}".format(e, query.strip())
            )
            self.connection.rollback()

    def insert(self, query, show=False):
        try:
            if show:
                return query
            else:
                self.connection.ping(True)
                self.cursor.execute(query)
                insert_id = self.cursor.lastrowid
                return insert_id
        except Exception as e:
            print(
                "MYSQL_EXCEPTION:\n{0}\nQuery:\n{1}".format(e, query.strip())
            )
            self.connection.rollback()

    def update(self, query, show=False):
        try:
            if show:
                return query
            else:
                self.connection.ping(True)
                self.cursor.execute(query)
                count = self.cursor.rowcount
                return count
        except Exception as e:
            print(
                "MYSQL_EXCEPTION:\n{0}\nQuery:\n{1}".format(e, query.strip())
            )
            self.connection.rollback()

    def delete(self, query, show=False):
        try:
            if show:
                return query
            else:
                self.connection.ping(True)
                self.cursor.execute(query)
                count = self.cursor.rowcount
                return count
        except Exception as e:
            print(
                "MYSQL_EXCEPTION:\n{0}\nQuery:\n{1}".format(e, query.strip())
            )
            self.connection.rollback()

    def transaction(self, query, show=False):
        try:
            if show:
                return query
            else:
                count = True
                self.connection.ping(True)
                self.connection.autocommit(False)
                query = query.split(';')
                for i in query:
                    self.cursor.execute(i)
                    count = self.cursor.rowcount

                if count:
                    self.connection.commit()
                else:
                    self.connection.rollback()

                return count
        except Exception as e:
            print(
                "MYSQL_EXCEPTION:\n{0}\nQuery:\n{1}".format(e, query.strip())
            )
            self.connection.close()

    def escape_string(self, data):
        return MySQLdb.escape_string(data)

    def __del__(self):
        try:
            self.connection.close()
        except Exception as e:
            print(f"{e}")

    def __str__(self) -> str:
        return f"""CONNECTION::\n    \
            HOST::{self.connection.get_host_info()}\n    \
            SERVER::{self.connection.get_server_info()}\n    \
            PROTO::{self.connection.get_proto_info()}\n    \
            WARNINGS::{self.connection.show_warnings()}\n\
            CURSOR::{self.cursor}\n"""
