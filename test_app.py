import pytest
from app import app as flask_app

@pytest.fixture
def app():
    """Create a new app instance for each test."""
    yield flask_app

@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()

def test_register_page_loads(client):
    """Test if the registration page (GET) loads correctly."""
    response = client.get('/register')
    assert response.status_code == 200
    assert b"User Registration" in response.data

def test_successful_registration(client):
    """Test if user registration (POST) redirects to the success page."""
    response = client.post('/register', data={
        'name': 'John Doe',
        'email': 'john.doe@example.com'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Registration Successful!" in response.data

def test_success_page_loads(client):
    """Test if the success page loads directly."""
    response = client.get('/success')
    assert response.status_code == 200
    assert b"Registration Successful!" in response.data
