from uuid import uuid4

import pymysql
from sqlalchemy.orm import Session

from abc import ABC
from app.bases.user import UserBase
from app.entities.user import User
from app.schemas.user import UserDTO
from app.services.user_history.user import ApiUser
from app.services.user_history.user_history import ApiHistory
from app.admin.security import get_hashed_password, generate_token, verify_password, myuuid

pymysql.install_as_MySQLdb()


class UserCrud(UserBase, ABC):

    def __init__(self, db: Session):
        self.db: Session = db

    def add_user(self, request_user: UserDTO): # userid, password
        riot_api = ApiUser()
        user = User(**request_user.dict())
        userid = self.find_uuid_by_userid(request_user=request_user)
        print(userid)
        if userid == "":
            user_list = riot_api.user_info(user.userid)
            user.uuid = user_list['uuid']
            user.userid = user_list['userid']
            user.tier = user_list['tier']
            user.win_rate = user_list['win_rate']
            user.most = user_list['most']
            user.level = user_list['level']
            user.password = get_hashed_password(user.password)
            is_success = self.db.add(user)
            print(is_success)
            self.db.commit()
            self.db.refresh(user)
            # user = self.db.query(User).filter(User.uuid == user_list['uuid']).first()
            # return {'uuid' : user.uuid, 'userid' : user.userid, 'tier' : user.tier, 'win_rate' : user.win_rate, 'most' : user.most, 'level' : user.level, 'password': user.password, 'token': user.token }
            return "회원가입 완료"

        else:
            return "소환사 명의로 가입할 수 없습니다."

    def login_user(self, request_user: UserDTO): # userid password
        userid = self.find_uuid_by_userid(request_user=request_user)
        if userid != "":
            request_user.userid = userid
            db_user = self.find_user_by_userid(request_user)
            print(db_user)
            verified = verify_password(plain_password=request_user.password,
                                       hashed_password=db_user.password)
            if verified:
                riot_api = ApiUser()
                user_list = riot_api.user_info(userid)
                new_token = generate_token(request_user.userid)
                request_user.token = new_token
                self.update_token(db_user, new_token)
                user = self.db.query(User).filter(User.uuid == user_list['uuid']).first()
                return {'uuid' : user.uuid, 'userid' : user.userid, 'tier' : user.tier, 'win_rate' : user.win_rate, 'most' : user.most, 'level' : user.level, 'token': user.token }
            else:
                return "비밀번호가 일치하지 않습니다"
        else:
            return "가입되지 않은 아이디 입니다.!"

    def logout_user(self, request_user: UserDTO): # token
        user = self.find_user_by_token(request_user)
        print(f' 유저 정보는 ;;;;{user}')
        is_success = self.db.query(User).filter(User.userid == user.userid). \
            update({User.token : ""}, synchronize_session=False)
        self.db.commit()
        print(f"토큰 삭제되면 1이 리턴 에상함 : {is_success}")
        return "로그아웃 성공입니다." if is_success != 0 else "로그아웃 실패입니다."

    def delete_user(self, request_user: UserDTO): # userid password token
        user = self.find_user_by_token(request_user)
        print(user.userid)
        is_success = self.db.query(User).filter(User.userid == user.userid). \
            delete(synchronize_session=False)
        self.db.commit()
        return "탈퇴 성공입니다." if is_success != 0 else "탈퇴 실패입니다."

    def update_user(self, request_user: UserDTO): # request_user는 userid token
        riot_api = ApiUser()
        user = self.find_user_by_token(request_user)
        user_list = riot_api.user_info(user.userid)
        self.db.query(User).filter(User.userid == user.userid) \
            .update({User.tier: user_list['tier'], User.win_rate : user_list['win_rate'], User.most : user_list['most'], User.level : user_list['level']}, synchronize_session=False)
        self.db.commit()
        self.db.refresh(user)
        user = self.db.query(User).filter(User.userid == user_list['userid']).first()
        return {'uuid': user.uuid, 'userid': user.userid, 'tier': user.tier, 'win_rate': user.win_rate,
                'most': user.most, 'level': user.level, 'password': user.password, 'token': user.token}

    def find_user_by_userid(self, request_user: UserDTO):
        user = User(**request_user.dict())
        userid = ApiHistory().summoner(user.userid)['nickname']
        return self.db.query(User).filter(User.userid == userid).one_or_none()

    def find_user_by_id_for_update(self, request_user: UserDTO):
        user = User(**request_user.dict())
        userid = ApiHistory().summoner(user.userid)['nickname']
        return self.db.query(User).filter(User.userid == userid).one_or_none()

    def update_token(self, db_user: User, new_token: str):
        is_success = self.db.query(User).filter(User.userid == db_user.userid)\
            .update({User.token: new_token}, synchronize_session=False)
        self.db.commit()
        self.db.refresh(db_user)
        return "" if is_success != 0 else "토큰 업데이트를 실패 하였습니다."

    def find_user_by_token(self, request_user: UserDTO) -> User:
        user = User(**request_user.dict())
        return self.db.query(User).filter(User.token == user.token).one_or_none()

    def find_uuid_by_userid(self, request_user: UserDTO):
        user = User(**request_user.dict())
        uuid = ApiHistory().summoner(user.userid)['uuid']
        db_user = self.db.query(User).filter(User.uuid == uuid).one_or_none()
        if db_user is not None:
            return db_user.userid
        else:
            return ""

    def match_token(self, request_user: UserDTO) -> bool:
        user = User(**request_user.dict())
        db_user = self.db.query(User).filter(User.token == user.token).one_or_none()
        return True if db_user != None else False


