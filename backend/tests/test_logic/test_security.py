from src.app.logic import security


def test_hashing():
    password = "I love inside jokes. I’d love to be a part of one someday"
    hashed = security.get_password_hash(password)

    assert security.verify_password(password, hashed)
    assert not security.verify_password(password[:-1] + "e", hashed)
    assert not security.verify_password("Something completely different", hashed)
