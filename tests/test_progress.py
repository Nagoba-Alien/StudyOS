from pathlib import Path

from app.intelligence.progress import (
    ProgressTracker,
)


def test_progress():

    test_file = Path(
        "data/test_progress.json"
    )

    # Remove old test data
    if test_file.exists():

        test_file.unlink()

    tracker = ProgressTracker(
        test_file
    )

    tracker.record(
        "CL 207",
        "Entropy",
        40,
        50,
    )

    tracker.record(
        "CL 207",
        "Entropy",
        70,
        75,
    )

    history = tracker.get_history(
        "CL 207",
        "Entropy",
    )

    assert len(history) == 2

    improvement = tracker.improvement(
        "CL 207",
        "Entropy",
    )

    assert improvement == 30
