from pydantic import BaseModel, Field
from typing import List, Optional

class AgentState(BaseModel):
    query: str
    vibe: Optional[str] = None
    plan: List[str] = Field(default_factory=list)
    nasa_results: Optional[str] = None
    library_receipts: List[str] = Field(default_factory=list)
    final_report: Optional[str] = None
    steps_taken: int = 0