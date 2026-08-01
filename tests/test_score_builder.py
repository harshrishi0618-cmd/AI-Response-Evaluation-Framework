from ai_response_eval.evaluators.scorer import ScoreBuilder


def test_penalty():
    builder = ScoreBuilder()

    builder.penalize(True, 3)

    assert builder.clamp() == 7


def test_no_penalty():
    builder = ScoreBuilder()

    builder.penalize(False, 3)

    assert builder.clamp() == 10


def test_multiple_penalties():
    builder = ScoreBuilder()

    builder.penalize(True, 3)
    builder.penalize(True, 5)

    assert builder.clamp() == 2


def test_score_never_negative():
    builder = ScoreBuilder()

    builder.penalize(True, 20)

    assert builder.clamp() == 0


def test_reward():
    builder = ScoreBuilder(initial_score=5)

    builder.reward(True, 2)

    assert builder.clamp() == 7
