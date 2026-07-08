import pytest


@pytest.fixture()
def client():
    import app as tiwap
    tiwap.dbm.reset_db()
    tiwap.app.config['TESTING'] = True
    with tiwap.app.test_client() as client:
        yield client


def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200


def test_login_empty_fields(client):
    response = client.post('/login', data={'username': '', 'password': ''})
    assert response.status_code == 200
    assert b'Fields Empty' in response.data


def test_login_invalid_credentials(client):
    response = client.post('/login', data={'username': 'admin', 'password': 'faux'})
    assert response.status_code == 200
    assert b'Invalid Credentials' in response.data


def test_login_valid_credentials_redirects_to_dashboard(client):
    response = client.post('/login', data={'username': 'admin', 'password': 'admin'})
    assert response.status_code == 302
    assert '/dashboard' in response.headers['Location']
