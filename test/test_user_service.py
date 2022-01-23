import bcrypt
import pytest
from sqlalchemy.exc import IntegrityError

from core.UserService import UserService
from data import User
from data.UserRepository import UserRepository


@pytest.fixture(scope="class")
def user_service():
    user_repo = UserRepository()
    return UserService(user_repo)


class TestUserService(object):
    def test_create(self, user_service: UserService):
        '''
            Test the user creation.
        '''
        # Test that clear password gets encrypted.
        user = User("gennar", "gennar@essex.ac.uk", "passw0rd")
        user_service.create(user)

        user_to_test = user_service.find_by_username("gennar")

        assert user_to_test.password == b'$2b$12$E7l3/2kbCaItkg85YhYBte/kLJXiMs3fxKw7GEpIrBW4EMNQ6kXCe'
        assert user_to_test.user_id is not None
        assert user_to_test.user_id > 0


        # For the same user('gennar'), it tests password match.
        pass_to_encrypt = "passw0rd".encode()
        from core import my_salt
        pass_to_test = bcrypt.hashpw(pass_to_encrypt, my_salt)

        user = user_service.find_by_username("gennar")

        assert pass_to_test == user.password

    def test_create_duplicates(self, user_service: UserService):
        '''
            Test that a duplicate username or email raise an exception.
        '''
        user1 = User("gennaro", "gennaro@essex.ac.uk", "passw0rd")
        user_service.create(user1)

        with pytest.raises(IntegrityError):
            user2 = User("gennaro", "gennaro@essex.ac.uk", "passw0rd")
            user_service.create(user2)

