from data import *

class PermissionRepository:
    @staticmethod
    def verify(entity_id: Integer, op_code: OpCode, user_id: Integer):
        session.query(Permission).filter_by(entity=entity_id, operation=op_code, user=user_id)
