import os

from enum import Enum
from urllib.parse import quote

from dotenv import load_dotenv


load_dotenv()



DB_HOST     = quote(os.getenv("DB_HOST"))
DB_PASSWORD = quote(os.getenv("DB_PASSWORD"))
DB_LOGIN    = quote(os.getenv("DB_LOGIN"))
DB_NAME     = quote(os.getenv("DB_NAME"))
DB_PORT     = quote(os.getenv("DB_PORT"))

BOT_TOKEN = os.getenv("BOT_TOKEN")
CONST_ENERGY = 70

class DatabaseType(Enum):
    USER = 'bot'


class DatabaseConfig:
    _configs = {
        DatabaseType.USER: f"mysql+aiomysql://{DB_LOGIN}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    }

    @classmethod
    def get_connection_string(cls, db_type: DatabaseType) -> str:
        return cls._configs.get(db_type)

class Gender(Enum):
    MAN   = "Чоловік"
    WOMAN = "Жінка"
    
class PositionCharacter(Enum):
    MIDFIELDER = "Півзахисник"
    DEFENDER   = "Захисник"
    GOALKEEPER = "Воротар"
    ATTACKER   = "Нападник" 
    
    
LEAGUES = [
    "🟢 Ліга новачків",
    "🔰 Ліга любителів",
    "⚪ Ліга аматорів",
    "🔶 Ліга напівпрофесіоналів",
    "🏅 Професійна ліга",
    "⚽ Друга ліга",
    "⚜️ Перша ліга",
    "🏆 Вища ліга",
    "🥇 Прем'єр-ліга"
]
