from enum import Enum
from typing import List, Optional

from uagents import Model

class UAgentResponseType(Enum):
    ERROR = "error"
    TEMPERATURE = "temperature"

class UAgentResponse(Model):
    type: UAgentResponseType
    agent_address: Optional[str]
    message: Optional[str]
    temperature: Optional[float]
    request_id: Optional[str]