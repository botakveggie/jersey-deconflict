from credentials import bot_token, bot_user_name,URL

import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\! This is the Jersey Deconflicting Bot!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    help_message = """Welcome to the Jersey Deconflicting Bot! This bot will inform you and your TM if a duplicate jersey number has been chosen! :)
    """
    update.message.reply_text(help_message)

def conflict_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /conflict is issued."""
    init_message = """Checking for conflict...
    """
    def conflict_exists():
        """checks if conflicting number exists"""
        return True
    update.message.reply_text(init_message)
    number_chosen = "Oh no! You cannot choose this number because it has already been chosen :'("
    number_ok = "Feel free to take this jersey number!"
    if conflict_exists():
        update.message.reply_text(number_chosen)
    else:
        update.message.reply_text(number_ok)        

def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(bot_token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("conflict", conflict_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()