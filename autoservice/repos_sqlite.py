import sqlite3
from typing import Optional, List
from datetime import datetime
from .interfaces import AppointmentRepository, CustomerRepository, InvoiceRepository
from .domain import Appointment, Customer, Invoice

def _dt_to_iso(dt: datetime) -> str:
    return dt.isoformat(timespec="seconds")

def _iso_to_dt(s: str) -> datetime:
    return datetime.fromisoformat(s)

class SQLiteCustomers(CustomerRepository):
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def add(self, cust: Customer) -> Customer:
        cur = self.conn.execute(
            "INSERT INTO customers(name, email) VALUES (?, ?)",
            (cust.name, cust.email)
        )
        cust.id = cur.lastrowid
        return cust

    def get_by_email(self, email: str) -> Optional[Customer]:
        row = self.conn.execute(
            "SELECT id, name, email FROM customers WHERE email = ?",
            (email,)
        ).fetchone()
        if not row: return None
        return Customer(id=row[0], name=row[1], email=row[2])

    def get(self, customer_id: int) -> Optional[Customer]:
        row = self.conn.execute(
            "SELECT id, name, email FROM customers WHERE id = ?",
            (customer_id,)
        ).fetchone()
        if not row: return None
        return Customer(id=row[0], name=row[1], email=row[2])

class SQLiteAppointments(AppointmentRepository):
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def add(self, appt: Appointment) -> Appointment:
        cur = self.conn.execute(
            "INSERT INTO appointments(customer_id, scheduled_at, notes) VALUES (?, ?, ?)",
            (appt.customer_id, _dt_to_iso(appt.scheduled_at), appt.notes)
        )
        appt.id = cur.lastrowid
        return appt

    def get(self, appt_id: int) -> Optional[Appointment]:
        row = self.conn.execute(
            "SELECT id, customer_id, scheduled_at, notes FROM appointments WHERE id = ?",
            (appt_id,)
        ).fetchone()
        if not row: return None
        return Appointment(id=row[0], customer_id=row[1], scheduled_at=_iso_to_dt(row[2]), notes=row[3])

    def list_for_customer(self, customer_id: int) -> List[Appointment]:
        rows = self.conn.execute(
            "SELECT id, customer_id, scheduled_at, notes FROM appointments WHERE customer_id = ?",
            (customer_id,)
        ).fetchall()
        return [Appointment(id=r[0], customer_id=r[1], scheduled_at=_iso_to_dt(r[2]), notes=r[3]) for r in rows]

class SQLiteInvoices(InvoiceRepository):
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def add(self, inv: Invoice) -> Invoice:
        cur = self.conn.execute(
            "INSERT INTO invoices(customer_id, appointment_id, amount_cents, created_at) VALUES (?,?,?,?)",
            (inv.customer_id, inv.appointment_id, inv.amount_cents, _dt_to_iso(inv.created_at))
        )
        inv.id = cur.lastrowid
        return inv
