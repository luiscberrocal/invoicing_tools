from datetime import datetime
from pathlib import Path
from typing import Optional

from pydantic import BaseModel


class JurisPerson(BaseModel):
    short_name: str
    name: str
    ruc: str
    dv: Optional[str]


class FiscalInvoice(BaseModel):
    number: int
    date: datetime
    ruc: str
    company: Optional[str]
    amount: float
    file: Optional[Path]
    person: Optional[JurisPerson]
