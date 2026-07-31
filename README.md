# AI Response Evaluation Framework

An open-source Python framework for evaluating Large Language Model (LLM) responses using modular evaluation metrics such as relevance, completeness, clarity, safety, and more.

The project is designed with extensibility in mind, allowing new evaluation metrics to be added with minimal changes to the core framework.

---

# Features

## Implemented

- Modular evaluation engine
- EvaluationRequest model
- EvaluationResult model
- EvaluationReport model
- BaseEvaluator interface
- RelevanceEvaluator
- CompletenessEvaluator
- Text preprocessing utilities
- Comprehensive unit tests

## Planned

- Clarity evaluator
- Safety evaluator
- Conciseness evaluator
- Hallucination evaluator
- JSON & Markdown reports
- CLI
- Gradio Web Interface
- Batch evaluation

---

# Architecture

```text
EvaluationRequest
        │
        ▼
EvaluationEngine
        │
        ▼
BaseEvaluator
        │
 ┌──────┴────────────┐
 ▼                   ▼
Relevance      Completeness
        │
        ▼
EvaluationResult
        │
        ▼
EvaluationReport
```

---

# Project Structure

```text
AI-Response-Evaluation-Framework/

├── data/
├── docs/
├── examples/
├── notebooks/
├── src/
│   └── ai_response_eval/
│       ├── evaluation/
│       ├── evaluators/
│       ├── models/
│       └── utils/
├── tests/
├── README.md
├── LICENSE
├── pyproject.toml
└── requirements.txt
```

---

# Installation

```bash
git clone https://github.com/<your-username>/AI-Response-Evaluation-Framework.git

cd AI-Response-Evaluation-Framework

python -m venv .venv

pip install -r requirements.txt

pip install -e .
```

---

# Example Usage

```python
from ai_response_eval.evaluation.engine import EvaluationEngine
from ai_response_eval.evaluators.relevance import RelevanceEvaluator
from ai_response_eval.evaluators.completeness import CompletenessEvaluator

engine = EvaluationEngine(
    evaluators=[
        RelevanceEvaluator(),
        CompletenessEvaluator(),
    ]
)

report = engine.evaluate(
    prompt="Explain machine learning.",
    response="Machine learning is a branch of AI that learns from data."
)

print(report.overall_score)
```

---

# Current Status

✅ Core framework completed

✅ Modular evaluator architecture

✅ Text preprocessing pipeline

✅ 20 passing unit tests

---

# Roadmap

## Version 0.1

- [x] Project setup
- [x] Evaluation engine
- [x] Relevance evaluator
- [x] Completeness evaluator
- [x] Unit testing

## Version 0.2

- [ ] Clarity evaluator
- [ ] Safety evaluator
- [ ] Conciseness evaluator

## Version 0.3

- [ ] CLI
- [ ] JSON reports
- [ ] Markdown reports

## Version 1.0

- [ ] Gradio interface
- [ ] Batch evaluation
- [ ] Plugin system
- [ ] Documentation

---

# Running Tests

```bash
pytest
```

Current test status:

```
20 tests passed
```

---

# Contributing

Contributions, suggestions, and bug reports are welcome.

Please open an issue before submitting major changes.

---

# License

MIT License