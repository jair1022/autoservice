import sqlite3
import pytest
from pathlib import Path
from datetime import datetime
from autoservice.infra_db import SQLiteDatabase
from autoservice.repos_sqlite import SQLiteCustomers, SQLiteAppointments, SQLiteInvoices

@pytest.fixture
def db_conn():
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON;")
    schema = Path("schema.sql").read_text(encoding="utf-8")
    conn.executescript(schema)
    yield conn
    conn.close()

@pytest.fixture
def sqlite_repos(db_conn):
    return {
        "customers": SQLiteCustomers(db_conn),
        "appointments": SQLiteAppointments(db_conn),
        "invoices": SQLiteInvoices(db_conn)
    }

@pytest.fixture
def db(db_conn):
    return SQLiteDatabase(db_conn)

# ---- Test doubles ----

class FakeTime:
    def __init__(self, fixed: datetime):
        self._now = fixed
    def now(self) -> datetime:
        return self._now

class SpyEmail:
    def __init__(self):
        self.calls = []
    def send(self, to: str, subject: str, body: str) -> None:
        self.calls.append({"to": to, "subject": subject, "body": body})

@pytest.fixture
def fake_time():
    return FakeTime(datetime(2025, 1, 1, 10, 30, 0))

@pytest.fixture
def spy_email():
    return SpyEmail()
