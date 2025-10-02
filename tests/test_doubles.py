from unittest.mock import Mock
from autoservice.repos_inmemory import InMemoryCustomers, InMemoryAppointments, InMemoryInvoices
from autoservice.services import AutoServiceManager
from autoservice.domain import Customer
from datetime import datetime

class FakePaymentGateway:
    def __init__(self): self.next_ok = True
    def set_next_result(self, ok: bool): self.next_ok = ok
    def charge(self, customer_id: int, amount_cents: int) -> bool:
        return self.next_ok

class SpyEmail:
    def __init__(self): self.calls = []
    def send(self, to, subject, body): self.calls.append((to, subject, body))

class FixedTime:
    def __init__(self, dt): self.dt = dt
    def now(self): return self.dt

class NoopDB:
    from contextlib import nullcontext
    def transaction(self): return self.nullcontext()

def test_mock_email_called_with_correct_data():
    email = Mock()
    time = FixedTime(datetime(2025,1,3,8,0,0))
    db = NoopDB()
    customers = InMemoryCustomers()
    appointments = InMemoryAppointments()
    invoices = InMemoryInvoices()
    c = customers.add(Customer(id=None, name="Mia", email="mia@acme.com"))

    svc = AutoServiceManager(time, email, db, customers, appointments, invoices)
    svc.create_appointment(customer_id=c.id, email=c.email)

    email.send.assert_called_once()
    to, subject, body = email.send.call_args[0]
    assert to == "mia@acme.com"
    assert "Cita creada" in subject
    assert "2025-01-03T08:00:00" in body

def test_spy_captures_all_emails():
    email = SpyEmail()
    time = FixedTime(datetime(2025,1,4,12,0,0))
    db = NoopDB()
    customers = InMemoryCustomers()
    appointments = InMemoryAppointments()
    invoices = InMemoryInvoices()
    c = customers.add(Customer(id=None, name="Neo", email="neo@acme.com"))

    svc = AutoServiceManager(time, email, db, customers, appointments, invoices)
    svc.create_appointment(customer_id=c.id, email=c.email)
    svc.create_appointment(customer_id=c.id, email=c.email)

    assert len(email.calls) == 2

def test_fake_gateway_example():
    gw = FakePaymentGateway()
    assert gw.charge(1, 1000) is True
    gw.set_next_result(False)
    assert gw.charge(1, 1000) is False
