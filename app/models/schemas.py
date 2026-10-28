from dataclasses import dataclass
from pydantic import BaseModel, Field

@dataclass
class Question:
    text: str


@dataclass
class Answer:
    text: str
    source: str | None = None


class AskRequest(BaseModel):
    question: str = Field(min_length=1)