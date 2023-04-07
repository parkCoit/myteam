from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.database import get_db
from app.entities.memo import Memo
from app.schemas.memo import MemoDTO
from app.cruds.memo import MemoCrud

from app.schemas.memo import MemoDTO

router = APIRouter()


@router.post("/create")
async def create_calendar(dto: MemoDTO, db: Session = Depends(get_db)):
    return JSONResponse(status_code=200, content=dict(msg=MemoCrud(db).create_memo_CRUD(request_memo=dto)))


@router.get("/read/{uuid}/{date}")
async def read_calendar(date: int, uuid: str, db: Session = Depends(get_db)):
    return JSONResponse(status_code=200, content=dict(msg=MemoCrud(db).read_memo_CRUD(date=date, uuid=uuid)))


@router.delete("/delete")
async def create_calendar(index: int, uuid: str, db: Session = Depends(get_db)):
    return JSONResponse(status_code=200, content=dict(msg=MemoCrud(db).delete_memo_CRUD(index=index, uuid=uuid)))
