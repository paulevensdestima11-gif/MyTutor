from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from app.extensions import db
from app.models import Lesson, Student

lessons_bp = Blueprint(
    "lessons",
    __name__,
    url_prefix="/lessons"
)


@lessons_bp.route("/")
def index():
    lessons = Lesson.query.order_by(
        Lesson.start_at.desc()
    ).all()

    return render_template(
        "lessons.html",
        lessons=lessons
    )


@lessons_bp.route("/add", methods=["GET", "POST"])
def add():

    students = Student.query.filter_by(
        active=True
    ).order_by(Student.name.asc()).all()

    if request.method == "POST":

        student_id = request.form.get("student_id", type=int)
        date_value = request.form.get("date")
        time_value = request.form.get("time")
        duration = request.form.get("duration", type=int)
        topic = request.form.get("topic", "").strip()
        notes = request.form.get("notes", "").strip()

        student = db.session.get(Student, student_id)

        if not student or not student.active:
            flash("Please select a valid active student.", "danger")
            return render_template(
                "add_lesson.html",
                students=students
            )

        if not date_value or not time_value or not topic:
            flash("Please complete all required fields.", "danger")
            return render_template(
                "add_lesson.html",
                students=students
            )

        if duration not in (30, 45, 60, 90, 120):
            flash("Invalid lesson duration.", "danger")
            return render_template(
                "add_lesson.html",
                students=students
            )

        try:
            start_at = datetime.strptime(
                f"{date_value} {time_value}",
                "%Y-%m-%d %H:%M"
            )
        except ValueError:
            flash("Invalid lesson date or time.", "danger")
            return render_template(
                "add_lesson.html",
                students=students
            )

        if start_at <= datetime.now():
            flash("Lesson must be scheduled in the future.", "danger")
            return render_template(
                "add_lesson.html",
                students=students
            )

        lesson = Lesson(
            student_id=student.id,
            start_at=start_at,
            duration=duration,
            topic=topic,
            attendance="scheduled",
            notes=notes
        )

        db.session.add(lesson)
        db.session.commit()

        flash("Lesson successfully scheduled!", "success")

        return redirect(url_for("lessons.index"))

    return render_template(
        "add_lesson.html",
        students=students
    )


@lessons_bp.route("/<int:lesson_id>/attendance", methods=["POST"])
def update_attendance(lesson_id):

    lesson = db.get_or_404(Lesson, lesson_id)

    attendance = request.form.get("attendance")

    allowed_values = {
        "scheduled",
        "present",
        "absent",
        "cancelled"
    }

    if attendance not in allowed_values:
        flash("Invalid attendance status.", "danger")
        return redirect(url_for("lessons.index"))

    lesson.attendance = attendance

    db.session.commit()

    flash("Attendance updated.", "success")

    return redirect(url_for("lessons.index"))