from pydantic import BaseModel


class EvaluationInput(BaseModel):
    prompt: str
    response: str
