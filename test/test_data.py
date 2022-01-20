# Test connectivity

def test_database_creation():
    import data
    result = data.session.query(data.User).all()
    assert len(result) == 0


def test_insert():
    import data
    data.session.begin()
    data.session.add(data.User("test_username", "email", "password1"))
    data.session.commit()

    result = data.session.query(data.User).all()
    print(f"Fetched user is {result[0]!r}")
    assert len(result) == 1
