import pytest

from helper.db_manager import DBManager


@pytest.fixture()
def dbm():
    manager = DBManager()
    manager.reset_db()
    return manager


def test_check_user_existing(dbm):
    assert dbm.check_user('admin') is True


def test_check_user_unknown(dbm):
    assert dbm.check_user('utilisateur_inconnu') is False


def test_check_login_valid_credentials(dbm):
    assert dbm.check_login(username='admin', password='admin') is True


def test_check_login_wrong_password(dbm):
    assert not dbm.check_login(username='admin', password='mauvais_mdp')


def test_check_login_unknown_user_returns_false(dbm):
    # Bugfix v1.0.1 : provoquait un TypeError (HTTP 500)
    assert dbm.check_login(username='utilisateur_inconnu', password='x') is False


def test_check_login_user_without_password_returns_false(dbm):
    # johndoe est seede avec un mot de passe NULL
    assert dbm.check_login(username='johndoe', password='') is False


def test_get_comments_seeded(dbm):
    comments = dbm.get_comments()
    assert len(comments) >= 3


def test_get_names_seeded(dbm):
    names = [row[0] for row in dbm.get_names()]
    assert 'Mark' in names


def test_save_and_read_comment(dbm):
    assert dbm.save_comment('commentaire de test CI') is True
    comments = [row[0] for row in dbm.get_comments()]
    assert 'commentaire de test CI' in comments
