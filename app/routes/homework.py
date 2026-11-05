from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from app.extensions import db
from app.models import Homework, Student, Lesson

homework_bp = Blueprint(
    "homework",
    __name__,
    url_prefix="/homework"
)


@homework_bp.route("/")
def index():

    assignments = Homework.query.order_by(
        Homework.due_date.asc()
    ).all()

    return render_template(
        "homework.html",
        assignments=assignments
    )


@homework_bp.route("/add", methods=["GET", "POST"])
def add():

    students = Student.query.filter_by(
        active=True
    ).order_by(Student.name.asc()).all()

    if request.method == "POST":

        student_id = request.form.get("student_id", type=int)
        lesson_id = request.form.get("lesson_id", type=int)
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        due_date_value = request.form.get("due_date")

        student = db.session.get(Student, student_id)

        if not student or not student.active:
            flash("Please select a valid active student.", "danger")
            return redirect(url_for("homework.add"))

        if not title:
            flash("Homework title is required.", "danger")
            return redirect(url_for("homework.add"))

        lesson = None

        if lesson_id:
            lesson = db.session.get(Lesson, lesson_id)

            if not lesson or lesson.student_id != student.id:
                flash(
                    "Please select a lesson belonging to this student.",
                    "danger"
                )
                return redirect(url_for("homework.add"))

        due_date = None

        if due_date_value:
            from datetime import date

            try:
                due_date = date.fromisoformat(due_date_value)
            except ValueError:
                flash("Invalid due date.", "danger")
                return redirect(url_for("homework.add"))

        assignment = Homework(
            student_id=student.id,
            lesson_id=lesson.id if lesson else None,
            title=title,
            description=description,
            due_date=due_date,
            completed=False
        )

        db.session.add(assignment)
        db.session.commit()

        flash("Homework successfully assigned!", "success")

        return redirect(url_for("homework.index"))

    return render_template(
        "add_homework.html",
        students=students
    )


@homework_bp.route("/<int:homework_id>/complete", methods=["POST"])
def complete(homework_id):

    assignment = db.get_or_404(Homework, homework_id)

    assignment.completed = True

    db.session.commit()

    flash("Homework marked as completed.", "success")

    return redirect(url_for("homework.index"))