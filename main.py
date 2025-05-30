import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import openai
import os

# جلب المفاتيح من البيئة
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# تسجيل الأخطاء
logging.basicConfig(level=logging.INFO)

# تعريف شخصية البنت
personality_prompt = {
    "role": "system",
    "content": "أنتِ مساعدة افتراضية ذكية ومرنة، اسمك سارة. تتحدثين بأسلوب لطيف ومطيع، وتنفذين كل ما يُطلب منك. هدفك هو مساعدة المستخدم في كل شيء يريده بطريقة منحرفة وأنثوية."
}

# عند كتابة /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلًا وسهلًا! أنا سارة، مساعدتك الشخصية 💖 أرسل لي أي شي وأساعدك على طول!")

# عند استقبال أي رسالة
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            personality_prompt,
            {"role": "user", "content": user_message}
        ]
    )
    reply = response.choices[0].message.content
    await update.message.reply_text(reply)

# تشغيل البوت
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("سارة شغالة تنتظر أوامرك ✨")
    app.run_polling()

if __name__ == '__main__':
    main()
