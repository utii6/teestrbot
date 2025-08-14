import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ---------- قراءة الحسابات ----------
with open('accounts.json', 'r') as f:
    data = json.load(f)

OWNER_ID = 5581457665

# ---------- واجهة التحكم للأزرار ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != OWNER_ID:
        await update.message.reply_text("مرحبا، البوت متوقف حاليا ✅")
        return

    # إنشاء أزرار للمالك
    keyboard = [
        [InlineKeyboardButton("قسم Instagram", callback_data='show_instagram')],
        [InlineKeyboardButton("قسم Telegram", callback_data='show_telegram')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("مرحباً بك يا البطل قاسم انت الأداري الوحيد والبوت يعمل لديك فقط...👑 اختر القسم:", reply_markup=reply_markup)

# ---------- التعامل مع الضغط على الأزرار ----------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'show_instagram':
        msg = "قسم Instagram:\n"
        for acc in data["instagram_accounts"]:
            msg += f"- {acc['username']}\n"
        await query.edit_message_text(msg)
    elif query.data == 'show_telegram':
        msg = "قسم Telegram:\n"
        for acc in data["telegram_accounts"]:
            msg += f"- {acc['phone']}\n"
        await query.edit_message_text(msg)

# ---------- تشغيل البوت ----------
TOKEN = "6217434623:AAGZqBjmVz-VZ6W0y0MXeN0pAtXyRjSZTNk"

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("البوت التجريبي مع لوحة تحكم شفافة يعمل الآن ✅")
app.run_polling()
