from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str  #bot's token
    admin_ids: list[int]    #admins's ids
    host: str
    database: str
    user: str
    password: str
    

@dataclass
class Config:
    tg_bot: TgBot
    
    
# creat function that read file .env and return instance of Config
def load_config(path: str or None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(
                    token=env('BOT_TOKEN'),
                    admin_ids=list(map(int, env.list('ADMIN_IDS'))),
                    host=env('HOST'),
                    database=env('DATABASE'),
                    user=env('USER'),
                    password=env('PASSWORD')))