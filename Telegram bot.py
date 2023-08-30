from typing import Final
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes, Updater, Application

TOKEN: Final = "6498118345:AAHo6Ow6lu42vTayZuonSUwFLirmpZQKkXU"
BOT_USERNAME: Final = "@scroll_message_bot"


# Commands

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello!')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Please type something so I can respond!')


async def set_message_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please enter the message you want to set:")
    context.user_data["waiting_for_message"] = True


async def send_announcement_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    custom_message = context.user_data.get("custom_message")
    if custom_message:
        group_ids = [5693780887, -1967973417]  # Replace with your group chat IDs
        for group_id in group_ids:
            await context.bot.send_message(group_id, custom_message)
        await update.message.reply_text("Announcement sent to groups!")
    else:
        await update.message.reply_text("No custom message set. Use /setmessage first.")


# Responses

async def handle_new_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("waiting_for_message"):
        message = update.message.text
        context.user_data["waiting_for_message"] = False
        context.user_data["custom_message"] = message
        await update.message.reply_text("Message set successfully!")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')


def main():
    print("Starting bot...")

    app = Application.builder().token(TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("setmessage", set_message_command))
    app.add_handler(CommandHandler("announce", send_announcement_command))

    # Register message handler
    app.add_handler(MessageHandler(filters.TEXT, handle_new_message))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))  # Add this line to process regular messages

    print("Polling...")
    app.run_polling(poll_interval=3)


if __name__ == "__main__":
    main()

"""TOKEN: Final = "6498118345:AAHo6Ow6lu42vTayZuonSUwFLirmpZQKkXU"
BOT_USERNAME: Final = "@scroll_message_bot"""