"""wrapper for the hoyolab.com gameRecord api

Majority of the endpoints require a cookie and a ds token, look at README.md for more info.
Some functions may have a raw parameter, this prettifies the output to a readable version.

https://github.com/thesadru/genshinstats
"""
import hashlib
import random
import re
import string
import time
from functools import lru_cache
from typing import List, Optional, Iterable
from urllib.parse import urljoin

from requests import Session

from .errors import *
from .pretty import *

session = Session()
session.headers.update({
    # required headers
    "x-rpc-app_version":"1.5.0",
    "x-rpc-client_type":"4",
    "x-rpc-language":"en-us",
    # authentications headers
    "cookie":"",
    "ds":"",
    # recommended headers
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9,cs;q=0.8",
    "origin": "https://webstatic-sea.hoyolab.com",
    "referer": "https://webstatic-sea.hoyolab.com/",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
})
DS_SALT = "6cqshh5dhw73bzxn20oexa9k516chk7s"
HOYOLABS_URL = "https://bbs-api-os.hoyolab.com/"


def set_cookie(account_id: int, cookie_token: str) -> None:
    """Basic configuration function, required for anything beyond search.
    
    Account id and cookie token must be copied from your browser's cookies.
    """
    session.headers['cookie'] = f'account_id={account_id}; cookie_token={cookie_token}'

def get_ds_token(salt: str) -> str:
    """Creates a new ds token.
    
    Uses an MD5 hash with a unique salt.
    """
    t = int(time.time()) # current seconds
    r = ''.join(random.sample(string.ascii_lowercase+string.digits, 6)) # 6 random chars
    c = hashlib.md5(f"salt={salt}&t={t}&r={r}".encode()).hexdigest() # hash and get hex
    return f'{t},{r},{c}'


def fetch_endpoint(endpoint: str, method: str='GET', headers: dict=None, **kwargs) -> dict:
    """Fetch an enpoint from the hoyolabs API.
    
    Takes in an endpoint or a url and kwargs that are later formatted to a query.
    A request is then sent and returns a parsed response.
    Includes error handling and ds token renewal.
    """
    url = urljoin(HOYOLABS_URL, endpoint) # join with base url
    session.headers['ds'] = get_ds_token(DS_SALT)
    if method == 'GET':
        r = session.get(url,headers=headers,params=kwargs)
    elif method == 'POST':
        r = session.post(url,headers=headers,json=kwargs)
    else:
        raise ValueError('Method can only be GET or POST')
    r.raise_for_status() # defaut HTTP Errors
    
    data = r.json()
    if data['data'] is not None: # success
        return data['data']
    
    # Custom HTTP Errors
    retcode,msg = data['retcode'],data['message']
    # UID
    if   retcode == 1009  and msg == "角色信息错误":
        raise InvalidUID('UID could not be found.')
    elif retcode == 10102 and msg == 'Data is not public for the user':
        raise DataNotPublic('User has set their data to be private. To enable go to https://www.hoyolab.com/genshin/accountCenter/gameRecord')
    # token
    elif retcode == -401  and msg == '请求异常':
        raise InvalidDS('Invalid DS token, might be expired.')
    elif retcode == 10001 and msg == 'Please login':
        raise NotLoggedIn('Login cookies have not been provided or are incorrect.')
    # other
    elif retcode == 1     and msg == 'Invalid schedule type':
        raise InvalidScheduleType('Invalid Spiral Abyss schedule type, can only be 1 or 2.')
    elif retcode == 2001  and msg == 'Duplicate operation or update failed':
        raise CannotCheckIn('Check-in is currently timed out, wait at least a day before checking-in again.')
    elif retcode == -1    and msg.endswith(' is not exists'):
        t,n = msg.split(':')
        raise InvalidItemID(f'{t} "{n.split()[0]}" does not exist.')
    else:
        raise GenshinStatsException(f"{retcode} Error ({data['message']}) for url: \"{r.url}\"")

def recognize_server(uid: int) -> str:
    """Recognizes which server a UID is from."""
    server = {
        1:'cn_gf01',
        5:'cn_qd01',
        6:'os_usa',
        7:'os_euro',
        8:'os_asia',
        9:'os_cht',
    }.get(int(str(uid)[0]))
    if server:
        return server
    else:
        raise InvalidUID("UID isn't associated with any server")

def search(keyword: str, size: int=20) -> dict:
    """Searches posts, topics and users.
    
    Takes in a keyword, replaces spaces with + and quotes other characters.
    Can return up to 20 results, based on size.
    """
    return fetch_endpoint("community/apihub/wapi/search",keyword=keyword,size=size,gids=2)

def check_in():
    """Checks in the user who's cookies are currently being used.
    
    This will give you points on hoyolab's site and also rewards in genshin.
    This also makes it possible to create an auto checkin.
    """
    fetch_endpoint("community/apihub/api/signIn",'POST',gids=2)

@lru_cache()
def get_langs() -> list:
    """Gets a list of translations for hoyolabs."""
    return fetch_endpoint("community/misc/wapi/langs",gids=2)['langs']

def get_community_user_info(community_uid: int) -> dict:
    """Gets community info of a user based on their community uid.
    
    Community info contains general data regarding the uid, nickname, introduction gender and so.
    It also contains stats for general community actions.
    
    You can get community id with `search`.
    """
    return fetch_endpoint("community/user/wapi/getUserFullInfo",uid=community_uid)

def get_record_card(community_uid: int) -> Optional[dict]:
    """Gets a game record card of a user based on their community uid.
    
    A record card contains data regarding the stats of a user for every server.
    Their UID for a given server is also included.
    In case the user has set their profile to be private, returns None.
    
    You can get community id with `search`.
    """
    cards = fetch_endpoint("game_record/card/wapi/getGameRecordCard",uid=community_uid,gids=2)['list']
    return cards[0] if cards else None

def get_uid_from_community(community_uid: int) -> Optional[int]:
    """Gets a uid with a community uid.
    
    This is so it's possible to search a user and then directly get the uid.
    In case the uid is private, returns None.
    """
    card = get_record_card(community_uid)
    return int(card['game_role_id']) if card else None

def get_user_info(uid: int, raw: bool=False) -> dict:
    """Gets game user info of a user based on their uid.
    
    Game user info contain the main nformation regarding a user.
    Contains owned characters, stats, city and world explorations and role.
    """
    server = recognize_server(uid)
    data = fetch_endpoint("game_record/genshin/api/index",server=server,role_id=uid)
    return data if raw else prettify_user_info(data)

def get_characters(uid: int, character_ids: List[int], lang: str='en-us', raw: bool=False) -> list:
    """Gets characters of a user set by their ids.
    
    Characters contain info about their level, constelation, weapon, and artifacts.
    Talents are not included.
    
    Change the language with lang, 
    possible langs can be found with get_langs() under the value field.
    """
    server = recognize_server(uid)
    data = fetch_endpoint(
        "game_record/genshin/api/character",'POST',
        headers={'x-rpc-language':lang},
        character_ids=character_ids,role_id=uid,server=server
    )["avatars"]
    return data if raw else prettify_characters(data)

def get_all_characters(uid: int, lang: str='en-us', raw: bool=False) -> list:
    """Gets all characters of a user.
    
    Characters contain info about their level, constelation, weapon, and artifacts.
    Talents are not included.
    
    Change the language with lang, 
    possible langs can be found with get_langs() under the value field.
    """
    characters = get_user_info(uid)['characters']
    return get_characters(uid,[i['id'] for i in characters],lang,raw)

def get_spiral_abyss(uid: int, previous: bool=False, raw: bool=False) -> dict:
    """Gets how far the user has gotten in spiral abyss and their season progress.
    
    Spiral abyss info contains their porgress, stats and individual completes.
    
    Every season these stats refresh and you can get the previous stats with `previous`.
    """
    server = recognize_server(uid)
    schedule_type = 2 if previous else 1
    data = fetch_endpoint("game_record/genshin/api/spiralAbyss",server=server,role_id=uid,schedule_type=schedule_type)
    return data if raw else prettify_spiral_abyss(data)

def is_game_uid(uid: int) -> bool:
    """Recognizes whether the uid is a game uid.
    
    Return True if it's a game uid, False if it's a community uid
    """
    return bool(re.fullmatch(r'[6789]\d{8}',str(uid)))


def get_active_players(page_size: int=20, offset: int=0) -> list:
    """Gets a list of recommended active players
    
    Max page size is 195, you cannot offset beyond that.
    """
    return fetch_endpoint("/community/user/wapi/recommendActive",gids=2,page_size=page_size,offset=offset)['list']

def get_public_players() -> Iterable[dict]:
    """Gets a list of players with public players.
    
    Returns a dict of their community uid, game uid and their game card.
    """
    players = get_active_players(page_size=0xffffffff)
    for player in players:
        community_uid = player['user']['uid']
        card = get_record_card(community_uid)
        if card is None:
            continue
        
        yield {
            'community_uid':community_uid,
            'uid':card['game_role_id'],
            'card':card
        }
