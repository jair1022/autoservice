import sqlite3
from contextlib import contextmanager
from .interfaces import Database

class SQLiteDatabase(Database):
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    @contextmanager
    def transaction(self):
        try:
            # SAVEPOINT permite transacciones anidadas (útil para tests)
            self.conn.execute("SAVEPOINT test_tx")
            yield
            self.conn.execute("RELEASE SAVEPOINT test_tx")
        except Exception:
            self.conn.execute("ROLLBACK TO SAVEPOINT test_tx")
            raise

