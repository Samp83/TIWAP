from helper.auth import Auth


def test_encode_decode_roundtrip():
    auth = Auth()
    token = auth.encode_auth_token('admin')
    payload = auth.decode_auth_token(token)
    assert payload['sub'] == 'admin'


def test_token_contains_expiration():
    auth = Auth()
    payload = auth.decode_auth_token(auth.encode_auth_token('johndoe'))
    assert payload['exp'] > payload['iat']


def test_insecure_token_roundtrip():
    auth = Auth()
    token = auth.insecure_auth_token('alice')
    assert auth.decode_insecure_auth_token(token) == 'alice'


def test_weak_token_roundtrip():
    auth = Auth()
    token = auth.weak_auth_token('bob')
    assert auth.decode_weak_auth_token(token) == 'bob'
