from decimal import Decimal
from datetime import datetime
from pathlib import Path
from typing import Optional, List

from sqlmodel import SQLModel, Field


class Client(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    short_name: str = Field(unique=True)
    name: str
    ruc: str = Field(unique=True)
    dv: Optional[str]
    emails: List[str]


class Payment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime
    amount: Decimal
    reference: str
    client_id: int = Field(default=None, foreign_key='client.id')


class FiscalInvoice(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    number: int
    date: datetime
    amount: Decimal
    file: Optional[Path]
    description: str
    date_emailed: Optional[datetime]
    client_id: int = Field(default=None, foreign_key='client.id')
    payment_id: int = Field(default=None, foreign_key='payment.id')
