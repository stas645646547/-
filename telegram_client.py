import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from integrations.language_detector import detect_language
from core.brain import process_user_message
from dotenv import load_dotenv

load_dotenv()
TG_TOKEN = os.getenv("TG_TOKEN")

def render_bot_response(response_dict):
    if not isinstance(response_dict, dict):
        return str(response_dict)
    answer = response_dict.get("answer", "")
    questions = response_dict.get("questions")
    text = answer
    if questions and questions.strip():
        text += f"\n\n❓ Уточняющие вопросы:\n{questions}"
    return text

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_lang = detect_language(user_message)
    user_id = update.effective_user.id

    response = await process_user_message(user_message, user_lang, user_id=user_id)

    if isinstance(response, dict):
        text = render_bot_response(response)
    else:
        text = str(response)
    await update.message.reply_text(text)

def main():
    application = ApplicationBuilder().token(TG_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("SuperLawyerBot запущен!")
    application.run_polling()

if __name__ == "__main__":
    main()
