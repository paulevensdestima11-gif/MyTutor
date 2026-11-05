from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)
from sqlalchemy import func

from app.extensions import db
from app.models import Student


students_bp = Blueprint(
    "students",
    __name__,
    url_prefix="/students"
)


@students_bp.route("/")
def index():
    students = Student.query.order_by(
        Student.name.asc()
    ).all()

    return render_template(
        "students.html",
        students=students
    )


@students_bp.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        level = request.form.get("level", "A1")
        goals = request.form.get("goals", "").strip()

        valid_levels = {
            "A1", "A2", "B1", "B2", "C1", "C2"
        }

        if not name:
            flash("Student name is required.", "danger")
            return render_template("add_student.html")

        if level not in valid_levels:
            flash("Please select a valid English level.", "danger")
            return render_template("add_student.html")

        if email and Student.query.filter(
            func.lower(Student.email) == email
        ).first():
            flash("This email is already registered.", "danger")
            return render_template("add_student.html")

        student = Student(
            name=name,
            email=email or None,
            level=level,
            goals=goals
        )

        db.session.add(student)
        db.session.commit()

        flash("Student successfully added!", "success")

        return redirect(url_for("students.index"))

    return render_template("add_student.html")