from sqlalchemy import Integer, Column, String, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True)
    createdOn = Column(DateTime)
    username = Column(String(50))
    email = Column(String(256))
    password = Column(String)
    cases = relationship("Case", back_populates="createdBy")
    evidences = relationship("Evidence", back_populates="createdBy")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.createdOn = datetime.now()

    def __repr__(self) -> str:
        return f"User(id={self.user_id!r}, username={self.username!r}, email={self.email!r})"


class Case(Base):
    __tablename__ = "case"
    case_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    createdBy = relationship("User", back_populates="cases")
    name = Column(String(50))
    description = Column(String(2000))
    deleted = Column(Boolean)
    deletedOn = Column(DateTime)
    updatedOn = Column(DateTime)
    createdOn = Column(DateTime)
    evidences = relationship("Evidence", back_populates="case")

    def __init__(self, user_id, name="", description=""):
        self.user_id = user_id
        self.name = name
        self.description = description
        self.deleted = False
        self.createdOn = datetime.now()

    def __repr__(self) -> str:
        return f"Case(id={self.case_id!r}, " \
               f"name={self.name!r}, " \
               f"desc={self.description!r}, " \
               f"createdBy={self.user_id!r}, " \
               f"createdOn={self.createdOn}, " \
               f"updatedOn={self.updatedOn!r}, " \
               f"isDeleted={self.deleted})"

class Evidence(Base):
    __tablename__ = "evidence"
    evidence_id = Column(Integer, primary_key=True)
    case_id = Column(Integer, ForeignKey('case.case_id'))
    case = relationship("Case", back_populates="evidences")
    user_id = Column(Integer, ForeignKey('user.user_id'))
    createdBy = relationship("User", back_populates="evidences")
    createdOn = Column(DateTime)
    content = Column(String)

    def __repr__(self) -> str:
        return f"Evidence(id={self.evidence_id!r}) belongs to {self.case!r})"
