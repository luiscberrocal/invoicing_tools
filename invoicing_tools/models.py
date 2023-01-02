from datetime import datetime
from pathlib import Path
from typing import Optional

from pydantic import BaseModel


class JurisPerson(BaseModel):
    name: str
    ruc: str
    dv: Optional[str]


class FiscalInvoice(BaseModel):
    date: datetime
    number: int
    ruc: str
    company: Optional[str]
    amount: float
    file: Optional[Path]
