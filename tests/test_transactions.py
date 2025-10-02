import pytest
from autoservice.services import AutoServiceManager
from autoservice.domain import Customer

def test_insert_appointment_persists_and_lists(db, sqlite_repos, fake_time, spy_email):
    customers = sqlite_repos["customers"]
    appointments = sqlite_repos["appointments"]
    invoices = sqlite_repos["invoices"]

    c = customers.add(Customer(id=None, name="Ana", email="ana@acme.com"))

    svc = AutoServiceManager(fake_time, spy_email, db, customers, appointments, invoices)
    appt = svc.create_appointment(customer_id=c.id, email=c.email, notes="Cambio de aceite")

    listed = appointments.list_for_customer(customer_id=c.id)
    assert len(listed) == 1
    assert listed[0].id == appt.id
    assert listed[0].scheduled_at == fake_time.now()

def test_fk_constraint_fails_for_nonexistent_customer(db, sqlite_repos, fake_time, spy_email):
    customers = sqlite_repos["customers"]
    appointments = sqlite_repos["appointments"]
    invoices = sqlite_repos["invoices"]

    svc = AutoServiceManager(fake_time, spy_email, db, customers, appointments, invoices)

    with pytest.raises(Exception):
        svc.create_appointment(customer_id=999, email="ghost@example.com")

def test_complex_transaction_all_or_nothing(db, sqlite_repos, fake_time, spy_email):
    customers = sqlite_repos["customers"]
    appointments = sqlite_repos["appointments"]
    invoices = sqlite_repos["invoices"]

    c = customers.add(Customer(id=None, name="Bob", email="bob@acme.com"))
    svc = AutoServiceManager(fake_time, spy_email, db, customers, appointments, invoices)

    appt, inv = svc.create_appointment_with_invoice(customer_id=c.id, email=c.email, amount_cents=250000)

    assert appt.id is not None
    assert inv.id is not None
    assert len(spy_email.calls) == 1
