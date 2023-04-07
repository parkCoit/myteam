from pydantic import BaseModel

class MemoDTO(BaseModel):
    tempindex: int
    uuid: str
    index: int
    content: str
    class Config:
        orm_mode = True

