from app.extensions import db
from app.models import Student, Lesson, Homework


def test_assign_homework(client, app):
    with app.app_context():
        student = Student(
            name="Homework Test Student",
            email="homework-test@example.com",
            level="A2"
        )

        db.session.add(student)
        db.session.commit()

        student_id = student.id

    response = client.post(
        "/homework/add",
        data={
            "student_id": str(student_id),
            "title": "Present Perfect Exercises",
            "description": "Complete exercises 1-10",
            "due_date": "2099-05-25"
        },
        follow_redirects=True
    )

    assert response.status_code == 200

    with app.app_context():
        homework = Homework.query.filter_by(
            title="Present Perfect Exercises"
        ).first()

        assert homework is not None
        assert homework.student_id == student_id
        assert homework.completed is False


def test_homework_cannot_be_linked_to_another_students_lesson(
    client, app
):
    with app.app_context():
        student_one = Student(
            name="Student One",
            email="one@example.com",
            level="A2"
        )

        student_two = Student(
            name="Student Two",
            email="two@example.com",
            level="B1"
        )

        db.session.add_all([student_one, student_two])
        db.session.commit()

        lesson = Lesson(
            student_id=student_one.id,
            start_at=__import__("datetime").datetime(2099, 5, 20, 14, 0),
            duration=60,
            topic="Grammar"
        )

        db.session.add(lesson)
        db.session.commit()

        student_two_id = student_two.id
        lesson_id = lesson.id

    response = client.post(
        "/homework/add",
        data={
            "student_id": str(student_two_id),
            "lesson_id": str(lesson_id),
            "title": "Invalid Assignment",
            "description": "Test"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Please select a lesson belonging to this student" in response.data

    with app.app_context():
        assert Homework.query.filter_by(
            title="Invalid Assignment"
        ).first() is None