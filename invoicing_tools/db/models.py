from decimal import Decimal
from datetime import datetime
from pathlib import Path
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship


class Client(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    short_name: str = Field(unique=True)
    name: str
    ruc: str = Field(unique=True)
    dv: Optional[str]
    emails: str
    fiscal_invoices: Optional[List['FiscalInvoice']] = Relationship(back_populates='client')


class Payment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime
    amount: Decimal
    reference: str
    client_id: int = Field(default=None, foreign_key='client.id')
    fiscal_invoices: List['FiscalInvoice'] = Relationship(back_populates='payment')


class FiscalInvoice(SQLModel, table=True):
    """https://sqlmodel.tiangolo.com/tutorial/relationship-attributes/back-populates/"""
    id: Optional[int] = Field(default=None, primary_key=True)
    number: int
    date: datetime
    amount: Decimal
    file: Optional[Path]
    description: str
    date_emailed: Optional[datetime]
    client_id: int = Field(default=None, foreign_key='client.id')
    client: Client = Relationship(back_populates='fiscal_invoices')
    payment_id: Optional[int] = Field(default=None, foreign_key='payment.id')
    payment: Optional[Payment] = Relationship(back_populates='fiscal_invoices')
