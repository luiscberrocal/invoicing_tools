from typing import Optional

import BaseModel as BaseModel


class JurisPerson(BaseModel):
    name: str
    ruc: str
    dv: Optional[str]



