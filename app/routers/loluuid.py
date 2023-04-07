import requests
from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse
from app.services.user_history.user_history import ApiHistory

router = APIRouter()


@router.get("/get-uuid/{nickname}")
async def get_uuid(nickname: str):
    try:
        user_data = ApiHistory().summoner(nickname=nickname)
        return JSONResponse(status_code=200, content={"uuid": user_data['uuid']})
    except:
        raise HTTPException(status_code=404, detail="SUMMONER_NOT_FOUND")
