from pydantic import BaseModel

class CalendarDTO(BaseModel):
    tempindex: int
    date: str
    start: str
    end: str
    content: str
    uuid: str
    class Config:
        orm_mode = True



