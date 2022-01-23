from data import *


class CaseRepository:
    PAGE_LIMIT = 1000

    def find_by_id(self, case_id: int) -> Case:
        return session.query(Case).get(case_id)

    def find_all(self) -> list[Case]:
        return session.query(Case).limit(self.PAGE_LIMIT).all()

    def find_all(self, page_number: int, page_size: int) -> list[Case]:
        offset = (page_number - 1) * page_size
        return session.query(Case).offset(offset).limit(page_size).all()

    def search(self):
        pass

    def delete_by_id(self, case_id: int) -> None:
        session.begin()
        case_to_delete = self.find_by_id(case_id)
        session.delete(case_to_delete)
        session.commit()

    def save(self, case: Case) -> int:
        inserted_id = case.case_id
        session.begin()
        if case.case_id is None:
            session.add(case)
            session.flush()
            inserted_id = case.case_id
        else:  # Existing case, just updating it.
            case.updatedOn = datetime.now()
            session.merge(case)
        session.commit()
        return inserted_id
