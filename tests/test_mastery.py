from app.adaptive.mastery import MasteryModel


def test_mastery():

    model = MasteryModel()

    score = model.estimate(
        "CL 207",
        "Assignment 1",
    )

    assert 0 <= score <= 100
