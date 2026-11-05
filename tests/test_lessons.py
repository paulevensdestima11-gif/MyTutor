from datetime import datetime

from app.extensions import db
from app.models import Student, Lesson


def create_student():
    student = Student(
        name="Lesson Test Student",
        email="lesson-test@example.com",
        level="A2",
        goals="Improve speaking"
    )

    db.session.add(student)
    db.session.commit()

    return student


def test_schedule_lesson(client, app):
    with app.app_context():
        student = create_student()
        student_id = student.id

    response = client.post(
        "/lessons/add",
        data={
            "student_id": str(student_id),
            "topic": "Present Perfect",
            "date": "2099-05-20",
            "time": "14:00",
            "duration": "60",
            "notes": "Grammar practice"
        },
        follow_redirects=True
    )

    assert response.status_code == 200

    with app.app_context():
        lesson = Lesson.query.filter_by(
            topic="Present Perfect"
        ).first()

        assert lesson is not None
        assert lesson.student_id == student_id
        assert lesson.duration == 60


def test_invalid_lesson_duration(client, app):
    with app.app_context():
        student = create_student()
        student_id = student.id

    response = client.post(
        "/lessons/add",
        data={
            "student_id": str(student_id),
            "topic": "Grammar",
            "date": "2099-05-20",
            "time": "14:00",
            "duration": "75"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Invalid lesson duration" in response.data