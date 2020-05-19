from enum import Enum

token = "1065792445:AAEHfx2MJTlsrhTbC6nlhTJPG4n3LyEoV8U"
db_file = "database.vdb"
travel_file = "travelling.db"


class States(Enum):
    S_START = "0"
    S_ENTER_NAME = "1"
    S_CHOOSE = "2"
    S_BUY_TRAVEL = "3"
    S_FINISH = "4"
    
