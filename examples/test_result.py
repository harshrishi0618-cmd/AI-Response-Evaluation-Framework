from ai_response_eval.models.result import EvaluationResult

result = EvaluationResult(
    metric="Relevance",
    score=9.2,
    feedback=[
        "Excellent response.",
        "Could include one example.",
    ],
)

print(result)
print(result.percentage)
print(result.passed)
