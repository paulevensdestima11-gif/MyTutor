from datetime import datetime

from flask import Blueprint, render_template

from app.models import Student, Lesson, Homework


dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.route("/")
def index():
    total_students = Student.query.filter_by(
        active=True
    ).count()

    upcoming_lessons = (
        Lesson.query
        .filter(
            Lesson.start_at >= datetime.now(),
            Lesson.attendance == "scheduled"
        )
        .order_by(Lesson.start_at.asc())
        .limit(5)
        .all()
    )

    pending_homework = Homework.query.filter_by(
        completed=False
    ).count()

    recent_students = (
        Student.query
        .filter_by(active=True)
        .order_by(Student.created_at.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "dashboard.html",
        total_students=total_students,
        upcoming_lessons=upcoming_lessons,
        pending_homework=pending_homework,
        recent_students=recent_students
    )