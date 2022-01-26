from data.PermissionRepository import PermissionRepository
from data import User, Case, OpCode


class Authorizer:
    def authorize(self, op_code: OpCode):
        return True


class AuthError(Exception):
    def __str__(self) -> str:
        return "Authorization exception"
