from sqlalchemy.orm import relationship

from app.database import Base
from sqlalchemy import Column, String, Integer


class User(Base):

    __tablename__ = "users"

    uuid = Column(String(100), primary_key=True)
    userid = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    tier = Column(String(30))
    win_rate = Column(String(30))
    most = Column(String(30))
    level = Column(Integer)
    token = Column(String(256))

    calendars = relationship('Calendar', back_populates='user')
    memos = relationship('Memo', back_populates='user')
    histories = relationship('History', back_populates='user')

    class Config:
        arbitrary_types_allowed = True

    def __str__(self):
        return f'index: {self.uuid}, \n '