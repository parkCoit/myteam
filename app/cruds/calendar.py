from abc import ABC
from typing import List

import pymysql
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.bases.memo import MemoBase
from app.entities.calendar import Calendar
from app.entities.memo import Memo
from app.schemas.calendar import CalendarDTO
from app.schemas.memo import MemoDTO

pymysql.install_as_MySQLdb()


class CalendarCrud(CalendarBase, ABC):

    def __init__(self, db: Session):
        self.db: Session = db

    def create_calendar_CRUD(self, request_calendar: CalendarDTO):
        db = self.db
        calendar = Calendar(**request_calendar.dict())
        db.add(calendar)
        db.commit()
        db.refresh(calendar)
        return "CREATE_SUCCESS"

    def read_calendar_CRUD(self, date: int, uuid: str):
        db = self.db
        calendar = db.query(Calendar).filter_by(date=date, uuid=uuid).order_by(Calendar.date.asc()).all()
        if not calendar:
            raise HTTPException(status_code=404, detail="CALENDAR_NOT_FOUND")
        return calendar

    def delete_calendar_CRUD(self, request_calendar: CalendarDTO):
        db_calendar = self.db.query(Memo).filter_by(tempindex=request_calendar.tempindex).first()
        if not db_calendar:
            raise HTTPException(status_code=404, detail="MEMO_NOT_FOUND")
        self.db.delete(db_calendar)
        self.db.commit()
        return "DELETE_SUCCESS"