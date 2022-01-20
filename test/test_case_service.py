# Test Case service functions
import pytest
import datetime

from core import CaseService
from core.CaseService import Authorizer
from data import Case
from data.CaseRepository import CaseRepository


@pytest.fixture(scope="class")
def case_service():
    case_repo = CaseRepository()
    autz = Authorizer()
    return CaseService.CaseService(case_repo, autz)


class TestCaseService(object):
    def test_create(self, case_service: CaseService.CaseService):
        case = Case(1, "testCase", "testDescription")
        new_id = case_service.save(case)
        print(f"{case}")
        assert new_id > 0
        assert new_id == case.case_id

    def test_edit(self, case_service: CaseService.CaseService):
        case = Case(1, "testCase", "testDescription")
        new_id = case_service.save(case)
        assert case.name == "testCase"

        case.name = "new_name"
        case_service.save(case)

        case_to_test = case_service.find_by_id(new_id)
        assert case_to_test == case
        assert case_to_test.name == "new_name"
        assert case_to_test.updatedOn is not None
        assert datetime.datetime.now() - case_to_test.updatedOn < datetime.timedelta(minutes=1)

    def test_delete(self, case_service: CaseService.CaseService):
        case = Case(1, "testCase", "testDescription")
        new_id = case_service.save(case)
        assert case.deleted is False
        assert case.deletedOn is None

        case_service.archive(case)

        case_to_test = case_service.find_by_id(new_id)
        assert case_to_test == case
        assert case_to_test.deleted is True
        assert case_to_test.deletedOn is not None
        assert datetime.datetime.now() - case_to_test.deletedOn < datetime.timedelta(minutes=1)
