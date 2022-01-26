import datetime

from core.Authorization import Authorizer, AuthError
from data import Case, OpCode
from data.CaseRepository import CaseRepository


class CaseService:
    _instance = None

    def __new__(cls, case_repository: CaseRepository, authorizer: Authorizer):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            cls.__init__(cls._instance, case_repository, authorizer)
        return cls._instance

    def __init__(self, case_repository: CaseRepository, authorizer: Authorizer):
        self.case_repo = case_repository
        self.authorizer = authorizer

    def find_by_id(self, case_id: int) -> Case:
        self.authorizer.authorize(OpCode.READ)
        return self.case_repo.find_by_id(case_id)

    def find_all(self, page_number: int = 1, page_size: int = 1000) -> list[Case]:
        self.authorizer.authorize(OpCode.READ)

        if page_size is None or page_number is None:
            return self.case_repo.find_all()

        return self.case_repo.find_all(page_number, page_size)

    def archive(self, case: Case):
        self.authorizer.authorize(OpCode.DELETE)
        case.deleted = True
        case.deletedOn = datetime.datetime.now()
        self.case_repo.save(case)

    def save(self, case: Case):
        self.authorizer.authorize(OpCode.UPDATE)
        return self.case_repo.save(case)
