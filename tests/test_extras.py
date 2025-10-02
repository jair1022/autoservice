import io
import sys
import sqlite3
import pytest
from datetime import datetime
from autoservice.infra_email import ConsoleEmail
from autoservice.infra_time import SystemTime
from autoservice.infra_db import SQLiteDatabase
from autoservice.repos_inmemory import InMemoryCustomers
from autoservice.repos_sqlite import SQLiteCustomers, SQLiteAppointments

# --- infra_email.py ---
def test_console_email_prints_output(capsys):
    email = ConsoleEmail()
    email.send("test@acme.com", "Hola", "Cuerpo del mensaje")
    captured = capsys.readouterr()
    assert "test@acme.com" in captured.out
    assert "Hola" in captured.out

# --- infra_time.py ---
def test_system_time_returns_datetime():
    time = SystemTime()
    now = time.now()
    assert isinstance(now, datetime)

# --- infra_db.py ---
def test_transaction_rollback_on_error(tmp_path):
    conn = sqlite3.connect(":memory:")
    db = SQLiteDatabase(conn)
    conn.execute("CREATE TABLE demo (id INTEGER PRIMARY KEY, name TEXT)")
    try:
        with db.transaction():
            conn.execute("INSERT INTO demo(name) VALUES (?)", ("ok",))
            raise RuntimeError("fail")
    except RuntimeError:
        pass
    rows = conn.execute("SELECT * FROM demo").fetchall()
    assert rows == []  # no se guardó nada por rollback

# --- repos_inmemory.py ---
def test_inmemory_get_and_get_by_email_none():
    repo = InMemoryCustomers()
    assert repo.get(999) is None
    assert repo.get_by_email("ghost@none.com") is None

# --- repos_sqlite.py ---
def test_sqlite_customers_get_and_none(db_conn):
    customers = SQLiteCustomers(db_conn)
    c = customers.add(type("Cust", (), {"id": None, "name": "Alice", "email": "alice@acme.com"})())
    assert customers.get(c.id).email == "alice@acme.com"
    assert customers.get(999) is None
    assert customers.get_by_email("no@none.com") is None

def test_sqlite_appointments_list_empty(db_conn):
    appts = SQLiteAppointments(db_conn)
    assert appts.list_for_customer(123) == []
