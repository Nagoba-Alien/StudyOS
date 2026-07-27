from app.exams.calendar import ExamCalendar


def test_exam_calendar():

    calendar = ExamCalendar()

    calendar.add_exam(
        "CL 207",
        "2026-08-15",
    )

    days = calendar.days_until_exam(
        "CL 207"
    )

    assert days >= 0
