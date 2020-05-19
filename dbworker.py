from vedis import Vedis
import bot_conf
############################
def get_current_state(user_id):
    with Vedis(bot_conf.db_file) as db:
        try:
            return db[user_id].decode()
        except KeyError:
            return bot_conf.States.S_START.value


def set_state(user_id, value):
    with Vedis(bot_conf.db_file) as db:
        try:
            db[user_id] = value
            return True
        except:
            print("Error1")
            return False
##############################        
def fill_travels(travels):
    i = 1
    with Vedis(bot_conf.travel_file) as tdb:
        try:
            for each in travels:
                #print(each + "!")
                tdb[i] = each
                i = i + 1
            return True
        except:
            print("Error2")
            return False
        
def get_travels():
    i = 1
    result = []
    with Vedis(bot_conf.travel_file) as tdb:
        try:
            while i <= 10:
                result.append(tdb[i].decode())
                i = i + 1
            return result
        except:
            print("Error3")
            return None

def get_travel(num):
    with Vedis(bot_conf.travel_file) as tdb:
        try:
            return tdb[num].decode()
        except KeyError:
            print("Error4")
            return None
###################################
def add_user(name, travel):
    with Vedis(bot_conf.user_file) as udb:
        try:
            print(name)
            if udb[name] == None:
                udb[name] = travel
            else:
                udb.append(name, travel)
            return True
        except:
            print("Error5")
            return False

def get_user(name):
    with Vedis(bot_conf.user_file) as udb:
        print(name)
        try:
            if udb[name] is None:
                print(111)
                return name + ", вы еще не приобрели ни одной поездки"
            else:
                return udb[name].decode()
        except:
            print("Error6")
            return None
