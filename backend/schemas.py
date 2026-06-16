from typing import Optional
from pydantic import BaseModel

class OrderUpdate(BaseModel):
    current_stage: str
    delay_reason: Optional[str] = None