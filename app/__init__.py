from flask import Flask, session, redirect, url_for

from config import Config
from app.extensions import db, migrate, csrf
from app.i18n import TRANSLATIONS


def create_app():
    app = Flask(__name__)

    # Load application configuration
    app.config.from_object(Config)
    csrf.init_app(app)

    # Initialize database and migrations
    db.init_app(app)
    migrate.init_app(app, db)

    # Import database models
    from app.models import (
        Student,
        Lesson,
        Homework,
        Progress,
        Material
    )

    # Import application routes
    from app.routes.dashboard import dashboard_bp
    from app.routes.students import students_bp
    from app.routes.lessons import lessons_bp
    from app.routes.homework import homework_bp

    # Register routes
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(lessons_bp)
    app.register_blueprint(homework_bp)

    # Language switching
    @app.route("/language/<lang>")
    def change_language(lang):
        if lang in ("en", "de"):
            session["language"] = lang

        return redirect(url_for("dashboard.index"))

    # Make translations available in templates
    @app.context_processor
    def inject_translations():
        language = session.get("language", "en")
        translations = TRANSLATIONS[language]

        return {
            "_": lambda key: translations.get(key, key)
        }

    return app