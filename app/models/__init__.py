from datetime import datetime, timezone

from app.extensions import db


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), unique=True)
    level = db.Column(db.String(5), nullable=False, default="A1")
    goals = db.Column(db.Text)
    active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    lessons = db.relationship(
        "Lesson",
        back_populates="student",
        cascade="all, delete-orphan"
    )

    homework = db.relationship(
        "Homework",
        back_populates="student",
        cascade="all, delete-orphan"
    )

    progress_records = db.relationship(
        "Progress",
        back_populates="student",
        cascade="all, delete-orphan"
    )


class Lesson(db.Model):
    __tablename__ = "lessons"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )
    start_at = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, default=60)
    topic = db.Column(db.String(150), nullable=False)
    attendance = db.Column(db.String(20), default="scheduled")
    notes = db.Column(db.Text)

    student = db.relationship("Student", back_populates="lessons")

    homework = db.relationship(
        "Homework",
        back_populates="lesson"
    )


class Homework(db.Model):
    __tablename__ = "homework"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )
    lesson_id = db.Column(
        db.Integer,
        db.ForeignKey("lessons.id")
    )
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.Date)
    completed = db.Column(db.Boolean, default=False, nullable=False)

    student = db.relationship("Student", back_populates="homework")
    lesson = db.relationship("Lesson", back_populates="homework")


class Progress(db.Model):
    __tablename__ = "progress"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )
    skill = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer)
    notes = db.Column(db.Text)
    recorded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    student = db.relationship(
        "Student",
        back_populates="progress_records"
    )


class Material(db.Model):
    __tablename__ = "materials"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    level = db.Column(db.String(5), nullable=False)
    topic = db.Column(db.String(100))
    file_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))