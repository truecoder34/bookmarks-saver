from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from storage_controller import check_if_id_exists, add_chat_id_to_storage, add_topic_by_id_to_storage, add_url_by_id_and_topic_to_storage, check_if_topic_exists, list_topics_by_id, list_bookmarks_by_id_and_topic, remove_url_by_id_and_topic, remove_topic_by_id
import os
import re

URL_REGEX = "^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$"
STATE = None
REPLIES = {
    "USER_NOT_EXISTS"   : "Hello, {}! You are new to our bot. Let's start our work ... ; Here is some information about bot - call > /help \n",
    "USER_EXISTS"       : "{}, welcome back! What action do you want to do?", 
    "HELP" : "It's a bot which will store all your improtant links on web-sources. \nCreate a topic, add urls in it. It is useful when you dont have time to read . \nNo problems, save it to me and come back later !",
    "HELP_TOPIC": "To addd a topic call command > /add_topic \nTo list your existing topics call command > /list_topic \nTo remove topic (with all bookmarks in it) call > /remove_topic",
    "HELP_BOOKMARK": "To addd a bookmark call command > /add_bookmark \nTo list your existing bookmarks in topic call command > /list_bookmark \nTo remove bookmark  call > /remove_bookmark",
}

def get_env_data_as_dict(path: str) -> dict:
    with open(path, 'r') as f:
       return dict(tuple(line.replace('\n', '').split('=')) for line
                in f.readlines() if not line.startswith('#'))

def check_url_matches(str, reg):
    is_match = bool(re.match(reg, str))
    return is_match


# function to handle the /start command
def start(update, context):
    first_name = update.message.chat.first_name
    print(update.message.chat)
    print(update.message.chat.id)
    print(update.message)
    if check_if_id_exists(update.message.chat.id):
        update.message.reply_text(REPLIES["USER_EXISTS"].format(first_name))
    else:
        update.message.reply_text(REPLIES["USER_NOT_EXISTS"].format(first_name))
        add_chat_id_to_storage(str(update.message.chat.id))




def help(update, context):
    update.message.reply_text(REPLIES["HELP"])
    update.message.reply_text(REPLIES["HELP_TOPIC"])
    update.message.reply_text(REPLIES["HELP_BOOKMARK"])



def error(update, context):
    update.message.reply_text('an error occured')

def text(update, context):
    text_received = update.message.text
    update.message.reply_text(f'did you said "{text_received}" ?')

################# CONTROLLERS CUSTOM ####################
####################### TOPIC ###########################
def add_topic(update, context):
    try:
        topic = context.args[0]
        print(topic)
        if check_if_topic_exists(str(update.message.chat.id), topic):
            update.message.reply_text('[INFO]: Topic already exists.{}'.format(topic))
        else:
            update.message.reply_text('[INFO]: Topic {} dont exists. adding it ... '.format(topic))
            add_topic_by_id_to_storage(str(update.message.chat.id), topic)
    except (IndexError, ValueError):
        update.message.reply_text('[ERROR] : There are no topic specified')

def list_topic(update, context):
    try:
        topics = list_topics_by_id(str(update.message.chat.id))
        for topic in topics:
            update.message.reply_text('[RESULT]: topic - {}. To list bookmarks call '.format(topic))
            update.message.reply_text('/list_bookmark {}'.format(topic))
    except (IndexError, ValueError):
        update.message.reply_text('[ERROR] : There are no topics')

def remove_topic(update, context):
    try:
        topic = context.args[0]
    except (IndexError, ValueError):
        update.message.reply_text('[ERROR] : There are no topic specified')

    try:
        if check_if_topic_exists(str(update.message.chat.id), topic):
           remove_topic_by_id(str(update.message.chat.id), topic)
           update.message.reply_text('[RESULT]: TOPIC WAS DELETED')
        else:
            update.message.reply_text('[RESULT]: NOTHING TO DELETE  ')
    except (IndexError, ValueError):
        update.message.reply_text('[ERROR] : ')

#########################################################
##################### Bookmark ##########################
def add_bookmark(update, context):
    try:
        topic = context.args[0]
        url = context.args[1]
        print(topic, " - ", url)
        # 1 - check if topic exists
        if check_if_topic_exists(str(update.message.chat.id), topic):
            update.message.reply_text('[INFO]: Topic {} already exists.'.format(topic))
        else:
            # create topic
            update.message.reply_text('[INFO]: Topic {} dont exists. adding it with bookmark...'.format(topic))
            add_topic_by_id_to_storage(str(update.message.chat.id), topic)
        
        # 2 - check if URL correct by regex 
        if check_url_matches(url, URL_REGEX):
            add_url_by_id_and_topic_to_storage(str(update.message.chat.id), topic, url)
            update.message.reply_text('[INFO]: Bookmark added to topic {}'.format(topic))
        else:
            update.message.reply_text('[ERROR] : Incorrect URL specified ')

    except (IndexError, ValueError):
        update.message.reply_text('[ERROR] : There are no topic or url specified')


def list_bookmark(update, context):
    try:
        topic = context.args[0]
    except (IndexError, ValueError):
        update.message.reply_text('[ERROR] : There are no topic specified')

    try:
        if check_if_topic_exists(str(update.message.chat.id), topic):
            bookmarks_in_topic = list_bookmarks_by_id_and_topic(str(update.message.chat.id), topic)
            for url in bookmarks_in_topic:
                update.message.reply_text('[RESULT]: - {}'.format(url))
            
            if len(bookmarks_in_topic) == 0:
                update.message.reply_text('[RESULT]: TOPIC IS EMPTY ')

        else:
            update.message.reply_text('[RESULT]: Specified topic doesnot exists in storage ')
    except (IndexError, ValueError):
        update.message.reply_text('[ERROR] : There are no topic specified')

def remove_bookmark(update, context):
    try:
        topic = context.args[0]
        url = context.args[1]
    except (IndexError, ValueError):
        update.message.reply_text('[ERROR] : There are no topic or url specified')

    try:
        if check_if_topic_exists(str(update.message.chat.id), topic):
           remove_url_by_id_and_topic(str(update.message.chat.id), topic, url)
           update.message.reply_text('[RESULT]: URL WAS DELETED')
        else:
            update.message.reply_text('[RESULT]: NOTHING TO DELETE  ')
    except (IndexError, ValueError):
        update.message.reply_text('[ERROR] : ')



def main():
    TOKEN = get_env_data_as_dict('.env')['TG_BOT_TOKEN']
    # create the updater, that will automatically create also a dispatcher and a queue to 
    # make them dialoge
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    # add handlers for start and help commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    
    dispatcher.add_handler(CommandHandler("add_topic", add_topic, pass_args=True))
    dispatcher.add_handler(CommandHandler("list_topic", list_topic, pass_args=True))
    dispatcher.add_handler(CommandHandler("remove_topic", remove_topic, pass_args=True))

    dispatcher.add_handler(CommandHandler("add_bookmark", add_bookmark, pass_args=True))
    dispatcher.add_handler(CommandHandler("list_bookmark", list_bookmark, pass_args=True))
    dispatcher.add_handler(CommandHandler("remove_bookmark", remove_bookmark, pass_args=True))



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