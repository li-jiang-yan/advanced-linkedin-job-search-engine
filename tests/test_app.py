"""Initial smoke tests for the Flask app."""


def test_create_app_sets_testing_mode(app):
    """The app factory should return a testing-ready Flask app."""
    assert app.testing is True
    assert app.name == "app"



def test_health_route_returns_ok(client):
    """The health endpoint should report a healthy status."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}
