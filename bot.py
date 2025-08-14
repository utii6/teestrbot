import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ---------- قراءة الحسابات ----------
with open('accounts.json', 'r') as f:
    data = json.load(f)

# OWNER_ID المدمج مباشرة للنسخة التجريبية
OWNER_ID = 5581457665

# ---------- رسالة الترحيب ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != OWNER_ID:
        await update.message.reply_text("مرحبا، البوت متوقف حاليا ✅")
    else:
        msg = "مرحبا بك يا المالك 👑\n\n"
        msg += "قسم Instagram:\n"
        for acc in data["instagram_accounts"]:
            msg += f"- {acc['username']}\n"
        msg += "\nقسم Telegram:\n"
        for acc in data["telegram_accounts"]:
            msg += f"- {acc['phone']}\n"
        await update.message.reply_text(msg)

# ---------- تشغيل البوت ----------
TOKEN = "6217434623:AAGZqBjmVz-VZ6W0y0MXeN0pAtXyRjSZTNk"

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("البوت التجريبي يعمل الآن ✅")
app.run_polling()
