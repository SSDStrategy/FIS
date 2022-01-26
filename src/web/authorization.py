from core.Authorization import Authorizer, AuthError
from data import OpCode, Case, User
from data.PermissionRepository import PermissionRepository


class DefaultAuthorizer(Authorizer):

    def authorize(self, op_code: OpCode, case: Case = None):
        current_user = self.login_context['user']

        if case is None or current_user is None:
            raise AuthError

        # The current user is the owner of the entity
        if current_user == case.createdBy:
            return True
        else:
            # the current user has permission for the requested operation
            permission = PermissionRepository.verify(case.get_id(), op_code, current_user.user_id)
            if permission is not None:
                return True

        raise AuthError


def get_user(request):
    jwt = request.cookies.get('jwt')

    # test user
    u = User("test1")
    u.user_id = 1
    return u
