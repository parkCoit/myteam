# from fastapi import APIRouter, Depends, HTTPException
# from fastapi.security import OAuth2PasswordRequestForm
# from sqlalchemy.orm import Session
#
# from app.database import get_db
# from app.cruds.login import get_user_by_id, authenticate_user
# from app.schemas.user import UserDTO
#
# router = APIRouter()
#
#
# @router.post("/login")
# async def login(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     db: Session = Depends(get_db)
# ):
#     user = await get_user_by_id(db, form_data.username)
#     if not user:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     if not authenticate_user(form_data.password, user.password):
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     return {"user": user}