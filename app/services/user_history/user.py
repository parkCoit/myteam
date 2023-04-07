import math

import pandas as pd
from riotwatcher import LolWatcher

from app.services.user_history.user_history import ApiHistory


class ApiUser(object):
    def __init__(self):
        global api_key, watcher, my_region
        api_key = "RGAPI-2d9f46bc-9615-4aa2-918b-a53b55078857"
        watcher = LolWatcher(api_key)
        my_region = "kr"

    def user_info(self, userid):
        user = watcher.summoner.by_name(my_region, userid)
        userid = user['name']
        uuid = user['puuid']
        match_id = watcher.match.matchlist_by_puuid(my_region, uuid, type='ranked')
        recent = []
        for i in range(len(match_id)):
            matches = watcher.match.by_id(my_region, match_id[i])
            metadata = matches['metadata']['participants']
            user_num = [i for i in range(0, 10) if metadata[i] == uuid]
            user_info = matches['info']["participants"][user_num[0]]
            champion_name = user_info['championName']
            recent.append(champion_name)
        print(recent)
        most = "" if recent == [] else max(set(recent), key=recent.count)
        # most = max(set(recent), key=recent.count)
        level = user['summonerLevel']
        leage = watcher.league.by_summoner(my_region, user['id'])
        print(range(len(leage)))
        num = -2
        for i in range(len(leage)):
            if leage[i]['queueType'] == 'RANKED_SOLO_5x5':
                num = i
        if num == -2 :
            user_list = {'uuid': uuid, 'userid': userid, 'tier': 'unranked', 'win_rate': '', 'most': '',
                         'level': level}
        else :
            tier = f"{leage[num]['tier']} {leage[num]['rank']}"
            win_rate = f"{int(leage[0]['wins'] / (leage[0]['losses'] + leage[0]['wins']) * 100)}%"
            user_list = {'uuid': uuid, 'userid': userid, 'tier': tier, 'win_rate': win_rate, 'most': most,
                         'level': level}
        print(user_list)
        return user_list




if __name__ == '__main__':
    ApiUser().user_info('hideonbush')
