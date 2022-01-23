import datetime

from core.Authorization import Authorizer, AuthError
from data import CaseRepository, Case, OpCode


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
