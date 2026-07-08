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


def test_login_unknown_user_no_crash(client):
    # Bugfix v1.0.1 : renvoyait HTTP 500 (TypeError dans check_login)
    response = client.post('/login', data={'username': 'utilisateur_inconnu', 'password': 'x'})
    assert response.status_code == 200
    assert b'Invalid Credentials' in response.data


def test_health_endpoint(client):
    # Nouvelle fonctionnalite v1.0.1
    from version import __version__
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json() == {'status': 'ok', 'version': __version__}


def test_version_displayed_on_index(client):
    # La version est affichee dans l'interface (header + footer)
    from version import __version__
    response = client.get('/')
    assert ('v' + __version__).encode() in response.data
