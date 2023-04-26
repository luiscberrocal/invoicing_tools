from datetime import datetime
from pathlib import Path
from typing import Optional

from pydantic import BaseModel
from sqlmodel import SQLModel, Field


class JurisPerson(BaseModel):
    short_name: str
    name: str
    ruc: str
    dv: Optional[str]
    email: str




class FiscalInvoice(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    number: int
    date: datetime
    ruc: str
    company: Optional[str]
    amount: float
    file: Optional[Path]
    person_id = Field(default=None, foreign_key='client.id')
    description: str
