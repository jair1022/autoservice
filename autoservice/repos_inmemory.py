from typing import Dict, List, Optional
from .interfaces import AppointmentRepository, CustomerRepository, InvoiceRepository
from .domain import Appointment, Customer, Invoice

class InMemoryCustomers(CustomerRepository):
    def __init__(self):
        self._data: Dict[int, Customer] = {}
        self._by_email: Dict[str, int] = {}
        self._seq = 1

    def add(self, cust: Customer) -> Customer:
        cust = Customer(id=self._seq, name=cust.name, email=cust.email)
        self._data[self._seq] = cust
        self._by_email[cust.email] = self._seq
        self._seq += 1
        return cust

    def get_by_email(self, email: str) -> Optional[Customer]:
        cid = self._by_email.get(email)
        return self._data.get(cid) if cid else None

    def get(self, customer_id: int) -> Optional[Customer]:
        return self._data.get(customer_id)

class InMemoryAppointments(AppointmentRepository):
    def __init__(self):
        self._data: Dict[int, Appointment] = {}
        self._seq = 1

    def add(self, appt: Appointment) -> Appointment:
        appt = Appointment(id=self._seq, customer_id=appt.customer_id, scheduled_at=appt.scheduled_at, notes=appt.notes)
        self._data[self._seq] = appt
        self._seq += 1
        return appt

    def get(self, appt_id: int) -> Optional[Appointment]:
        return self._data.get(appt_id)

    def list_for_customer(self, customer_id: int) -> List[Appointment]:
        return [a for a in self._data.values() if a.customer_id == customer_id]

class InMemoryInvoices(InvoiceRepository):
    def __init__(self):
        self._data: Dict[int, Invoice] = {}
        self._seq = 1

    def add(self, inv: Invoice) -> Invoice:
        inv = Invoice(id=self._seq, customer_id=inv.customer_id, appointment_id=inv.appointment_id,
                      amount_cents=inv.amount_cents, created_at=inv.created_at)
        self._data[self._seq] = inv
        self._seq += 1
        return inv
