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
async def create_memo(dto: MemoDTO, db: Session = Depends(get_db)):
    return JSONResponse(status_code=200, content=dict(msg=MemoCrud(db).create_memo_CRUD(request_memo=dto)))


@router.get("/read/{uuid}/{index}")
async def read_memo(index: int, uuid: str, db: Session = Depends(get_db)):
    return JSONResponse(status_code=200, content=dict(msg=MemoCrud(db).read_memo_CRUD(index=index, uuid=uuid)))


@router.put("/update")
async def create_memo(dto: MemoDTO, db: Session = Depends(get_db)):
    return JSONResponse(status_code=200, content=dict(msg=MemoCrud(db).update_memo_CRUD(request_memo=dto)))


@router.delete("/delete/{uuid}/{index}")
async def create_memo(index: int, uuid: str, db: Session = Depends(get_db)):
    return JSONResponse(status_code=200, content=dict(msg=MemoCrud(db).delete_memo_CRUD(index=index, uuid=uuid)))
