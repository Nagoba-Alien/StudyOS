from app.storage.history import RevisionHistory


def test_history():

    history = RevisionHistory()

    before = history.get(
        course="CL 207",
        title="Assignment 1",
    )

    old_count = before["review_count"]

    history.update(
        course="CL 207",
        title="Assignment 1",
        confidence=1,
        completed=False,
    )

    item = history.get(
        course="CL 207",
        title="Assignment 1",
    )

    assert item is not None

    assert item["completed"] is False

    assert item["confidence"] == 1

    assert item["review_count"] == old_count + 1
