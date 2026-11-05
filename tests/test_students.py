
import re


def test_students_page_loads(client):
    response = client.get("/students/")
    assert response.status_code == 200


def test_add_student_page_loads(client):
    response = client.get("/students/add")
    assert response.status_code == 200


def test_student_can_be_registered(client):
    response = client.post(
        "/students/add",
        data={
            "name": "John Smith",
            "email": "john@example.com",
            "level": "A2",
            "goals": "Improve speaking"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"John Smith" in response.data


def test_student_registration_rejects_missing_csrf_token(app):
    app.config["WTF_CSRF_ENABLED"] = True

    client = app.test_client()

    response = client.post(
        "/students/add",
        data={
            "name": "Test Student",
            "email": "test@example.com",
            "level": "A2",
            "goals": "Improve English"
        }
    )

    assert response.status_code == 400


def test_student_registration_accepts_valid_csrf_token(app):
    app.config["WTF_CSRF_ENABLED"] = True

    client = app.test_client()

    response = client.get("/students/add")
    assert response.status_code == 200

    html = response.get_data(as_text=True)

    match = re.search(
        r'name="csrf_token"\s+value="([^"]+)"',
        html
    )

    assert match is not None, "CSRF token not found in form"

    csrf_token = match.group(1)

    response = client.post(
        "/students/add",
        data={
            "csrf_token": csrf_token,
            "name": "Jane Smith",
            "email": "jane@example.com",
            "level": "B1",
            "goals": "Improve grammar"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Jane Smith" in response.data
