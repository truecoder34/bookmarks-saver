from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from storage_controller import check_if_id_exists
import os

URL_REGEX = "^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$"
STATE = None
REPLIES = {
    "USER_NOT_EXISTS"   : "Hello, {}! You are new to our bot. Let's start our work ... ; What action do you want to do? ",
    "USER_EXISTS"       : "{}, welcome back! What action do you want to do?", 
    "HELP" : "It's a bot which will store all your improtant links on web-sources. \nCreate a topic, add urls in it. It is useful when you dont have time to read . \nNo problems, save it to me and come back later !"
}

def get_env_data_as_dict(path: str) -> dict:
    with open(path, 'r') as f:
       return dict(tuple(line.replace('\n', '').split('=')) for line
                in f.readlines() if not line.startswith('#'))



# function to handle the /start command
def start(update, context):
    first_name = update.message.chat.first_name
    print(update.message.chat)
    print(update.message.chat.id)
    if check_if_id_exists(update.message.chat.id):
        update.message.reply_text(REPLIES["USER_EXISTS"].format(first_name))
    else:
        update.message.reply_text(REPLIES["USER_NOT_EXISTS"].format(first_name))



def help(update, context):
    update.message.reply_text(REPLIES["HELP"])


def error(update, context):
    update.message.reply_text('an error occured')

def text(update, context):
    text_received = update.message.text
    update.message.reply_text(f'did you said "{text_received}" ?')

################# CONTROLLERS CUSTOM ####################
####################### TOPIC ###########################
def add_topic(update, context):
    update.message.reply_text('add_topic')
def list_topic(update, context):
    update.message.reply_text('list_topicd')
def remove_topic(update, context):
    update.message.reply_text('remove_topic')

#########################################################
##################### Bookmark ##########################
def add_bookmark(update, context):
    update.message.reply_text('add_bookmark')
def list_bookmark(update, context):
    update.message.reply_text('list_bookmark')
def remove_bookmark(update, context):
    update.message.reply_text('remove_bookmark')

#########################################################
############### READ \ WRITE JSON STORAGE ###############



def main():
    TOKEN = get_env_data_as_dict('.env')['TG_BOT_TOKEN']
    # create the updater, that will automatically create also a dispatcher and a queue to 
    # make them dialoge
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    # add handlers for start and help commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    
    dispatcher.add_handler(CommandHandler("add_topic", add_topic))
    dispatcher.add_handler(CommandHandler("list_topic", list_topic))
    dispatcher.add_handler(CommandHandler("remove_topic", remove_topic))

    dispatcher.add_handler(CommandHandler("add_bookmark", add_bookmark))
    dispatcher.add_handler(CommandHandler("list_bookmark", list_bookmark))
    dispatcher.add_handler(CommandHandler("remove_bookmark", remove_bookmark))



    # add an handler for normal text (not commands)
    dispatcher.add_handler(MessageHandler(Filters.text, text))
    # add an handler for errors
    dispatcher.add_error_handler(error)
    # start your shiny new bot
    updater.start_polling()
    # run the bot until Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()