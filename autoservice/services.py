from datetime import datetime
from .interfaces import TimeProvider, EmailService, AppointmentRepository, CustomerRepository, InvoiceRepository, Database
from .domain import Appointment, Invoice

class AutoServiceManager:
    def __init__(self,
                 time_provider: TimeProvider,
                 email_service: EmailService,
                 db: Database,
                 customers: CustomerRepository,
                 appointments: AppointmentRepository,
                 invoices: InvoiceRepository):
        self.time = time_provider
        self.email = email_service
        self.db = db
        self.customers = customers
        self.appointments = appointments
        self.invoices = invoices

    def create_appointment(self, customer_id: int, email: str, when: datetime | None = None, notes: str = "") -> Appointment:
        scheduled_at = when or self.time.now()
        appt = Appointment(id=None, customer_id=customer_id, scheduled_at=scheduled_at, notes=notes)
        appt = self.appointments.add(appt)
        self.email.send(email, "Cita creada", f"Su cita es el {scheduled_at.isoformat()}")
        return appt

    def create_appointment_with_invoice(self, customer_id: int, email: str, amount_cents: int,
                                        when: datetime | None = None, notes: str = "") -> tuple[Appointment, Invoice]:
        scheduled_at = when or self.time.now()
        with self.db.transaction():
            appt = self.appointments.add(
                Appointment(id=None, customer_id=customer_id, scheduled_at=scheduled_at, notes=notes)
            )
            inv = self.invoices.add(
                Invoice(id=None, customer_id=customer_id, appointment_id=appt.id, amount_cents=amount_cents,
                        created_at=self.time.now())
            )
            self.email.send(email, "Cita confirmada", f"Cita {appt.id} y factura {inv.id} creada.")
            return appt, inv
