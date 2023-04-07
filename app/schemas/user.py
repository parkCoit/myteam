from typing import Optional

from pydantic import BaseModel


class UserVo(BaseModel):

    class Config:
        arbitrary_types_allowed = True


class UserDTO(UserVo):
    uuid: Optional[str]
    userid: Optional[str]
    password : Optional[str]
    tier : Optional[str]
    win_rate : Optional[str]
    most : Optional[str]
    level : Optional[int]
    token : Optional[str]


    def __str__(self):
        return f'uuid: {self.uuid}, \n ' \
               f'userid: {self.userid},' \
               f'tier: {self.tier},' \
               f'win_rate: {self.win_rate},' \
               f'most: {self.most},' \
               f'level: {self.level},' \
               f'password: {self.password}' \
               f'token: {self.token},'