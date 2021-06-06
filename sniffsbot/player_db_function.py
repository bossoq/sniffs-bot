from bot_init import client_init
from db_connect import Database


class player_db_function:
    def __init__(self):
        self.db = Database(filename='./player.db', table='players')
        self.client = client_init()

    def check_cur_userstat(self, username):
        if self.db.check_exist(username): return self.db.retrieve(username)
        else: return {}

    async def create_player(self, username):
        db_key = ['username', 'coin']
        user_stat = [username, 0]
        user_stat_dict = dict(zip(db_key, user_stat))
        self.db.insert(user_stat_dict)
        print(f'create {username}')

    async def db_coin(self, username, coin):
        if self.db.check_exist(username):
            user_stat = self.check_cur_userstat(username)
            user_stat['coin'] += coin
            self.db.update(user_stat)
            print(f'{username} get {coin} coin(s)')
        else:
            await self.create_player(username)
            user_stat = self.check_cur_userstat(username)
            user_stat['coin'] += coin
            self.db.update(user_stat)
            print(f'{username} get {coin} coin(s)')

    async def player_payday(self, user_list, coin):
        for username in user_list: await self.db_coin(username.lower(), coin)
