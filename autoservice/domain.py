from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Customer:
    id: Optional[int]
    name: str
    email: str

@dataclass
class Appointment:
    id: Optional[int]
    customer_id: int
    scheduled_at: datetime
    notes: str = ""

@dataclass
class Invoice:
    id: Optional[int]
    customer_id: int
    appointment_id: int
    amount_cents: int
    created_at: datetime
