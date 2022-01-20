import datetime

from data import CaseRepository, Case

import enum


class OpCode(enum.Enum):
    CREATE = 1
    UPDATE = 2
    DELETE = 3
    READ = 4
    SEARCH = 5


class Authorizer:
    def authorize(self, op_code: OpCode):
        return True


class DefaultAuthorizer(Authorizer):

    def __init__(self, jwt):
        self.loginContext = jwt

    def authorize(self, op_code: OpCode):
        return super().authorize(op_code)


class AuthError(Exception):
    def __str__(self) -> str:
        return "Authorization exception"


class CaseService:

    def __init__(self, case_repository: CaseRepository, authorizer: Authorizer):
        self.case_repo = case_repository
        self.authorizer = authorizer

    def find_by_id(self, case_id: int) -> Case:
        if self.authorizer.authorize(OpCode.READ):
            return self.case_repo.find_by_id(case_id)
        # to log
        raise AuthError

    def find_all(self) -> list[Case]:
        if self.authorizer.authorize(OpCode.READ):
            return self.case_repo.find_all()
        # to log
        raise AuthError

    def find_all(self, page_number: int, page_size: int) -> list[Case]:
        if self.authorizer.authorize(OpCode.READ):
            return self.case_repo.find_all(page_number, page_size)
        # to log
        raise AuthError

    def archive(self, case: Case):
        if self.authorizer.authorize(OpCode.DELETE):
            case.deleted = True
            case.deletedOn = datetime.datetime.now()
            self.case_repo.save(case)
        else:
            raise AuthError

    def save(self, case: Case):
        if self.authorizer.authorize(OpCode.UPDATE):
            return self.case_repo.save(case)
        else:
            raise AuthError
