from data.PermissionRepository import PermissionRepository
from data import User, Case, OpCode


class Authorizer:
    def authorize(self, op_code: OpCode):
        return True


class DefaultAuthorizer(Authorizer):

    def __init__(self, user: User):
        self.login_context = {
            "user": user
        }

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


class AuthError(Exception):
    def __str__(self) -> str:
        return "Authorization exception"
