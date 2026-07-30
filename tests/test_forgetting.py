from app.adaptive.forgetting import ForgettingModel


def test_forgetting():

    model = ForgettingModel()

    score = model.estimate(
        "CL 207",
        "Assignment 1",
    )

    assert 0 <= score <= 100
