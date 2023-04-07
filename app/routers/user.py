from fastapi import APIRouter, Depends
from riotwatcher import ApiError
from sqlalchemy.orm import Session
from fastapi import HTTPException
from starlette.responses import JSONResponse, RedirectResponse

from app.cruds.user import UserCrud
from app.database import get_db
from app.schemas.user import UserDTO

router = APIRouter()


@router.post("/add", status_code=201)
async def add_user(dto: UserDTO, db : Session = Depends(get_db)):
    try:
        return JSONResponse(status_code=200,
                            content=dict(
                                msg=UserCrud(db).add_user(request_user=dto)
                            ))
    except ApiError as e:
        if e.response.status_code == 404:
            return {"msg": "아이디가 존재하지 않습니다"}
        else:
            return {"Error": e}


@router.post("/login", status_code=200)
async def login_user(dto: UserDTO, db: Session = Depends(get_db)):
    try:
        return JSONResponse(status_code=200,
                            content=dict(
                                msg=UserCrud(db).login_user(request_user=dto)))

    except ApiError as e:
        if e.response.status_code == 404:
            return {"msg": "아이디가 존재하지 않습니다"}
        else:
            return {"Error": e}


@router.post("/logout", status_code=200)
async def logout_user(dto: UserDTO, db: Session = Depends(get_db)):
    try:
        return JSONResponse(status_code=200,
                            content=dict(
                                msg=UserCrud(db).logout_user(request_user=dto)))

    except ApiError as e:
        if e.response.status_code == 404:
            return {"msg": "아이디가 존재하지 않습니다"}
        else:
            return {"Error": e}


@router.delete("/delete", tags=['age'])
async def remove_user(dto: UserDTO, db: Session = Depends(get_db)):
    try:
        if UserCrud(db).match_token(request_user=dto):
            return JSONResponse(status_code=200,
                                content=dict(
                                    msg=UserCrud(db).delete_user(dto)))
        else:
            RedirectResponse(url='/no-match-token', status_code=302)

    except ApiError as e:
        if e.response.status_code == 404:
            return {"msg": "아이디가 존재하지 않습니다"}
        else:
            return {"Error": e}


@router.put("/modify")
async def modify_user(dto: UserDTO, db: Session = Depends(get_db)):
    try:
        if UserCrud(db).match_token(request_user=dto):
            return JSONResponse(status_code=200,
                            content=dict(
                                msg=UserCrud(db).update_user(dto)))
        else:
            RedirectResponse(url='/no-match-token', status_code=302)

    except ApiError as e:
        if e.response.status_code == 404:
            return {"msg": "아이디가 존재하지 않습니다"}
        else:
            return {"Error": e}

