from pydantic import BaseModel


class EvaluationInput(BaseModel):
    prompt: str
    response: str


class MetricResult(BaseModel):
    metric_name: str
    score: float
    feedback: str
    passed: bool


class EvaluationOutput(BaseModel):
    overall_score: float
    grade: str
    status: str
    results: list[MetricResult]
