import configparser
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

config = configparser.ConfigParser()
config.read("config.ini")

bot_token = str(config["Telegram"]["bot_token"])
channel_id = str(config["Telegram"]["channel_id"])
bot = telepot.Bot(bot_token)



def prettyMsg(m):
    msg = "League: " + m['League'] + "\n" + "Match: " +"*"+ m[
        "Match"]+"*" + "\n" + "Score: " + m["Score"] + "\n" + "GT: " + str(
            round(m['GT'], 2)) + "\n" + "Time: " + str(
                m["Time"]) + "'" + "\n" + "Over: " + str(
                    m["Over"]) + "\n" + "ODDS: " + str(
                        m["ODDS"]) 
    return msg


def notifSignals(msg1, msg2, msg3):
    m = prettyMsg(msg1) + "\n" + prettyMsg(msg2) + "\n" + prettyMsg(msg3)+ "\n" +"Wait for Goals ,TOTALS ODDS :"+"*"+str(round(msg1["ODDS"]*msg2["ODDS"]*msg3["ODDS"],2))+"*"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                  [InlineKeyboardButton(text='Match1', url=msg1["Link"])],[InlineKeyboardButton(text='Match2', url=msg2["Link"])],[InlineKeyboardButton(text='Match2', url=msg3["Link"])]  ])
    bot.sendMessage(channel_id, m, reply_markup=keyboard,parse_mode= 'Markdown' )
