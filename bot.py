import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

ACCOUNTS_FILE = 'accounts.json'
OWNER_ID = 5581457665

# ---------- تحميل الحسابات ----------
def load_accounts():
    with open(ACCOUNTS_FILE, 'r') as f:
        return json.load(f)

def save_accounts(data):
    with open(ACCOUNTS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# ---------- لوحة التحكم الرئيسية ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != OWNER_ID:
        await update.message.reply_text("مرحبا حبيبي تحتاج شي تعال هنا @E2E12 ، البوت متوقف حاليا ✅")
        return

    keyboard = [
        [InlineKeyboardButton("Instagram", callback_data='menu_instagram')],
        [InlineKeyboardButton("Telegram", callback_data='menu_telegram')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("مرحباً بك يا المالك قاسم وحدك بهذا البوت👑 اختر القسم:", reply_markup=reply_markup)

# ---------- التعامل مع الضغط على الأزرار ----------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = load_accounts()

    if query.data == 'menu_instagram':
        keyboard = [[InlineKeyboardButton(f"{acc['username']}", callback_data=f"insta_{i}") ] for i, acc in enumerate(data['instagram_accounts'])]
        keyboard.append([InlineKeyboardButton("إضافة حساب جديد", callback_data='insta_add')])
        keyboard.append([InlineKeyboardButton("عودة للقائمة الرئيسية", callback_data='main_menu')])
        await query.edit_message_text("قسم Instagram:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == 'menu_telegram':
        keyboard = [[InlineKeyboardButton(f"{acc['phone']}", callback_data=f"tele_{i}") ] for i, acc in enumerate(data['telegram_accounts'])]
        keyboard.append([InlineKeyboardButton("إضافة حساب جديد", callback_data='tele_add')])
        keyboard.append([InlineKeyboardButton("عودة للقائمة الرئيسية", callback_data='main_menu')])
        await query.edit_message_text("قسم Telegram:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == 'main_menu':
        await start(query, context)

    # هنا يمكن تطوير الضغط على الحسابات لخيارات إضافية لاحقًا
    elif query.data.startswith('insta_add') or query.data.startswith('tele_add'):
        await query.edit_message_text("أرسل البيانات بصيغة: username,password أو phone,api_id,api_hash")
        context.user_data['adding'] = query.data  # لتحديد القسم القادم

# ---------- استقبال رسالة لإضافة الحساب ----------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'adding' in context.user_data:
        section = context.user_data['adding']
        parts = update.message.text.split(',')
        data = load_accounts()

        if section == 'insta_add':
            if len(parts) != 2:
                await update.message.reply_text("خطأ في الصيغة. استخدم: username,password")
                return
            data['instagram_accounts'].append({'username': parts[0], 'password': parts[1]})
            save_accounts(data)
            await update.message.reply_text(f"تمت إضافة حساب Instagram: {parts[0]}")
        elif section == 'tele_add':
            if len(parts) != 3:
                await update.message.reply_text("خطأ في الصيغة. استخدم: phone,api_id,api_hash")
                return
            data['telegram_accounts'].append({'phone': parts[0], 'api_id': int(parts[1]), 'api_hash': parts[2]})
            save_accounts(data)
            await update.message.reply_text(f"تمت إضافة حساب Telegram: {parts[0]}")

        del context.user_data['adding']

# ---------- تشغيل البوت ----------
TOKEN = "6217434623:AAGZqBjmVz-VZ6W0y0MXeN0pAtXyRjSZTNk"

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

print("البوت التجريبي المتقدم مع لوحة تحكم شفافة يعمل الآن ✅")
app.run_polling()
