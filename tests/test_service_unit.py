from unittest.mock import Mock
from datetime import datetime
from autoservice.services import AutoServiceManager
from autoservice.repos_inmemory import InMemoryCustomers, InMemoryAppointments, InMemoryInvoices
from autoservice.domain import Customer

class NoopDB:
    from contextlib import nullcontext
    def transaction(self): return self.nullcontext()

class FixedTime:
    def __init__(self, dt): self.dt = dt
    def now(self): return self.dt

def test_unit_service_uses_injected_time_and_email():
    time = FixedTime(datetime(2025, 1, 2, 9, 0, 0))
    email = Mock()
    db = NoopDB()
    customers = InMemoryCustomers()
    appointments = InMemoryAppointments()
    invoices = InMemoryInvoices()

    c = customers.add(Customer(id=None, name="Zoe", email="zoe@acme.com"))

    svc = AutoServiceManager(time, email, db, customers, appointments, invoices)
    appt = svc.create_appointment(customer_id=c.id, email=c.email, notes="Alineación")

    assert appt.scheduled_at == time.now()
    email.send.assert_called_once()
    to, subject, body = email.send.call_args[0]
    assert to == c.email
    assert "Cita creada" in subject
