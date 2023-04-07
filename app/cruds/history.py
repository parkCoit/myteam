from abc import ABC

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.bases.history import HistoryBase
from app.database import engine, conn
from app.entities.history import History
from app.schemas.history import HistoryDTO
from app.services.user_history.user_history import ApiHistory


class HistoryCrud(HistoryBase, ABC):

    def __init__(self, db: Session):
        self.db: Session = db

    def get_history(self, request_history: HistoryDTO):  # userid
        user = History(**request_history.dict())
        db_history = self.find_user(request_history=request_history)
        if db_history == "" :
            return "잘못된 값 입니다"
        else :
            user_count = self.db.query(History).filter(History.userid == db_history).count()
            user_history = self.db.query(History).filter(History.userid == db_history).all()
            userid_ls, match_id_ls, champion_name_ls, result_ls, kills_ls, deaths_ls, assists_ls, kda_ls, position_ls, game_minute_ls, game_candle_ls \
                = list(), list(), list(), list(), list(), list(), list(), list(), list(), list(), list()
            for i in range(user_count):
                userid = user_history[i].userid
                matchid = user_history[i].matchid
                champion = user_history[i].champion
                result = user_history[i].result
                kills = user_history[i].kills
                deaths = user_history[i].deaths
                assists = user_history[i].assists
                kda = user_history[i].kda
                position = user_history[i].position
                game_minute = user_history[i].minute
                game_candle = user_history[i].candle
                userid_ls.append(userid)
                match_id_ls.append(matchid)
                champion_name_ls.append(champion)
                result_ls.append(result)
                kills_ls.append(kills)
                deaths_ls.append(deaths)
                assists_ls.append(assists)
                kda_ls.append(kda)
                position_ls.append(position)
                game_minute_ls.append(game_minute)
                game_candle_ls.append(game_candle)

            return [{'userid': userid_ls[i], 'champion': champion_name_ls[i], 'result': result_ls[i], 'kills': kills_ls[i],
                    'deaths': deaths_ls[i], 'assists': assists_ls[i], 'kda' : kda_ls[i], 'position': position_ls[i], 'minute' : game_minute_ls[i], 'candle' : game_candle_ls[i] } for i in range(user_count)]

    def update_userid(self, request_history: HistoryDTO):
        user_id = self.find_userid_by_api(request_history=request_history)
        user_uuid = self.find_uuid_by_api(request_history=request_history)
        self.db.query(History).filter(History.uuid == user_uuid).update({History.userid : user_id})
        self.db.commit()
        user_name = self.db.query(History).filter(History.userid == user_id).first()
        return user_name.userid

    def update_history(self, request_history: HistoryDTO):  # userid
        # user_id = self.find_userid_by_api(request_history=request_history)
        user_uuid = self.find_uuid_by_api(request_history=request_history)
        self.db.query(History).filter(History.uuid == user_uuid). \
            delete(synchronize_session=False)
        self.db.commit()
        user_id = self.df_to_sql_by_userid(request_history=request_history)
        db_history = self.db.query(History).filter(History.userid == user_id).first()
        user_count = self.db.query(History).filter(History.userid == db_history.userid).count()
        user_history = self.db.query(History).filter(History.userid == db_history.userid).all()
        userid_ls, match_id_ls, champion_name_ls, result_ls, kills_ls, deaths_ls, assists_ls, kda_ls, position_ls, game_minute_ls, game_candle_ls \
            = list(), list(), list(), list(), list(), list(), list(), list(), list(), list(), list()
        for i in range(user_count):
            userid = user_history[i].userid
            matchid = user_history[i].matchid
            champion = user_history[i].champion
            result = user_history[i].result
            kills = user_history[i].kills
            deaths = user_history[i].deaths
            assists = user_history[i].assists
            kda = user_history[i].kda
            position = user_history[i].position
            game_minute = user_history[i].minute
            game_candle = user_history[i].candle
            userid_ls.append(userid)
            match_id_ls.append(matchid)
            champion_name_ls.append(champion)
            result_ls.append(result)
            kills_ls.append(kills)
            deaths_ls.append(deaths)
            assists_ls.append(assists)
            kda_ls.append(kda)
            position_ls.append(position)
            game_minute_ls.append(game_minute)
            game_candle_ls.append(game_candle)

        return [{'userid': userid_ls[i], 'champion': champion_name_ls[i], 'result': result_ls[i], 'kills': kills_ls[i],
                    'deaths': deaths_ls[i], 'assists': assists_ls[i], 'kda' : kda_ls[i], 'position': position_ls[i], 'minute' : game_minute_ls[i], 'candle' : game_candle_ls[i] } for i in range(user_count)]

    def find_user(self, request_history: HistoryDTO):
        user_id = self.find_userid_by_api(request_history=request_history)
        user_uuid = self.find_uuid_by_api(request_history=request_history)
        db_user = self.db.query(History).filter(History.userid == user_id).first()
        if db_user is not None:
            return db_user.userid
        else :
            if self.db.query(History).filter(History.uuid == user_uuid).first() is not None: # update
                return self.update_userid(request_history)
            elif self.find_userid_by_api is "": return ""
            else : return self.df_to_sql_by_userid(request_history=request_history)

    def df_to_sql_by_userid(self, request_history: HistoryDTO):
        riot_api = ApiHistory()
        user_id = self.find_userid_by_api(request_history=request_history)
        play_list = riot_api.play_list(user_id)
        table_name = 'history'
        play_list.to_sql(table_name, con=engine, if_exists='append', index=False)
        self.db.commit()
        asdf = self.db.query(History).filter(History.userid == user_id).first()
        return asdf.userid

    def find_userid_by_api(self, request_history: HistoryDTO):
        riot_api = ApiHistory()
        user = History(**request_history.dict())
        user_list = riot_api.summoner(user.userid)
        print(user_list)
        return user_list['nickname']

    def find_uuid_by_api(self, request_history: HistoryDTO):
        riot_api = ApiHistory()
        user = History(**request_history.dict())
        user_list = riot_api.summoner(user.userid)
        print(user_list)
        return user_list['uuid']











