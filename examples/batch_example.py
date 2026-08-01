from ai_response_eval.batch.evaluator import BatchEvaluator
from ai_response_eval.batch.io import BatchExporter, BatchLoader
from ai_response_eval.evaluation.engine import EvaluationEngine
from ai_response_eval.evaluators.clarity import ClarityEvaluator
from ai_response_eval.evaluators.completeness import CompletenessEvaluator
from ai_response_eval.evaluators.conciseness import ConcisenessEvaluator
from ai_response_eval.evaluators.relevance import RelevanceEvaluator
from ai_response_eval.evaluators.safety import SafetyEvaluator

engine = EvaluationEngine(
    evaluators=[
        RelevanceEvaluator(),
        CompletenessEvaluator(),
        ClarityEvaluator(),
        SafetyEvaluator(),
        ConcisenessEvaluator(),
    ]
)

requests = BatchLoader.load_csv("examples/sample_dataset.csv")

reports = BatchEvaluator(engine).evaluate(requests)

BatchExporter.save_csv(
    reports,
    "examples/results.csv",
)

print("Results saved to examples/results.csv")
