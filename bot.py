import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from datetime import datetime

ACCOUNTS_FILE = 'accounts.json'
LOG_FILE = 'log.json'
OWNER_ID = 5581457665

# ---------- تحميل الحسابات ----------
def load_accounts():
    with open(ACCOUNTS_FILE, 'r') as f:
        return json.load(f)

def save_accounts(data):
    with open(ACCOUNTS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# ---------- تسجيل العمليات ----------
def log_action(action):
    try:
        with open(LOG_FILE, 'r') as f:
            logs = json.load(f)
    except:
        logs = []

    logs.append({"time": datetime.now().isoformat(), "action": action})
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=2)

# ---------- لوحة التحكم الرئيسية ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != OWNER_ID:
        await update.message.reply_text("مرحبا حبيبي تحتاج شي تعال @E2E12 ، البوت متوقف حاليا ✅")
        return

    keyboard = [
        [InlineKeyboardButton("Instagram", callback_data='menu_instagram')],
        [InlineKeyboardButton("Telegram", callback_data='menu_telegram')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("مرحباً بك يا المالك وحدك داخل غرفة BatMan💎 👑 اختر القسم:", reply_markup=reply_markup)

# ---------- التعامل مع الضغط على الأزرار ----------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = load_accounts()

    # العودة للقائمة الرئيسية
    if query.data == 'main_menu':
        await start(query, context)
        return

    # ---------- Instagram ----------
    if query.data == 'menu_instagram':
        keyboard = [[InlineKeyboardButton(f"{acc['username']}", callback_data=f"insta_{i}") ] for i, acc in enumerate(data['instagram_accounts'])]
        keyboard.append([InlineKeyboardButton("إضافة حساب جديد", callback_data='insta_add')])
        keyboard.append([InlineKeyboardButton("عودة للقائمة الرئيسية", callback_data='main_menu')])
        await query.edit_message_text("قسم Instagram:", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    elif query.data.startswith('insta_'):
        idx = int(query.data.split('_')[1])
        acc = data['instagram_accounts'][idx]
        keyboard = [
            [InlineKeyboardButton("حذف الحساب", callback_data=f"insta_del_{idx}")],
            [InlineKeyboardButton("عودة للقائمة Instagram", callback_data='menu_instagram')],
            [InlineKeyboardButton("عودة للقائمة الرئيسية", callback_data='main_menu')]
        ]
        await query.edit_message_text(f"Instagram: {acc['username']}", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    elif query.data.startswith('insta_del_'):
        idx = int(query.data.split('_')[2])
        username = data['instagram_accounts'][idx]['username']
        del data['instagram_accounts'][idx]
        save_accounts(data)
        log_action(f"تم حذف حساب Instagram: {username}")
        await query.edit_message_text(f"تم حذف الحساب: {username}")
        return

    elif query.data == 'insta_add':
        await query.edit_message_text("أرسل بيانات الحساب بصيغة: username,password")
        context.user_data['adding'] = 'insta'
        return

    # ---------- Telegram ----------
    if query.data == 'menu_telegram':
        keyboard = [[InlineKeyboardButton(f"{acc['phone']}", callback_data=f"tele_{i}") ] for i, acc in enumerate(data['telegram_accounts'])]
        keyboard.append([InlineKeyboardButton("إضافة حساب جديد", callback_data='tele_add')])
        keyboard.append([InlineKeyboardButton("عودة للقائمة الرئيسية", callback_data='main_menu')])
        await query.edit_message_text("قسم Telegram:", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    elif query.data.startswith('tele_'):
        idx = int(query.data.split('_')[1])
        acc = data['telegram_accounts'][idx]
        keyboard = [
            [InlineKeyboardButton("حذف الحساب", callback_data=f"tele_del_{idx}")],
            [InlineKeyboardButton("عودة للقائمة Telegram", callback_data='menu_telegram')],
            [InlineKeyboardButton("عودة للقائمة الرئيسية", callback_data='main_menu')]
        ]
        await query.edit_message_text(f"Telegram: {acc['phone']}", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    elif query.data.startswith('tele_del_'):
        idx = int(query.data.split('_')[2])
        phone = data['telegram_accounts'][idx]['phone']
        del data['telegram_accounts'][idx]
        save_accounts(data)
        log_action(f"تم حذف حساب Telegram: {phone}")
        await query.edit_message_text(f"تم حذف الحساب: {phone}")
        return

    elif query.data == 'tele_add':
        await query.edit_message_text("أرسل بيانات الحساب بصيغة: phone,api_id,api_hash")
        context.user_data['adding'] = 'tele'
        return

# ---------- استقبال رسالة لإضافة الحساب ----------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'adding' in context.user_data:
        section = context.user_data['adding']
        parts = update.message.text.split(',')
        data = load_accounts()

        if section == 'insta':
            if len(parts) != 2:
                await update.message.reply_text("خطأ في الصيغة. استخدم: username,password")
                return
            data['instagram_accounts'].append({'username': parts[0], 'password': parts[1]})
            save_accounts(data)
            log_action(f"تمت إضافة حساب Instagram: {parts[0]}")
            await update.message.reply_text(f"تمت إضافة حساب Instagram: {parts[0]}")

        elif section == 'tele':
            if len(parts) != 3:
                await update.message.reply_text("خطأ في الصيغة. استخدم: phone,api_id,api_hash")
                return
            data['telegram_accounts'].append({'phone': parts[0], 'api_id': int(parts[1]), 'api_hash': parts[2]})
            save_accounts(data)
            log_action(f"تمت إضافة حساب Telegram: {parts[0]}")
            await update.message.reply_text(f"تمت إضافة حساب Telegram: {parts[0]}")

        del context.user_data['adding']

# ---------- تشغيل البوت ----------
TOKEN = "6217434623:AAGZqBjmVz-VZ6W0y0yMXeN0pAtXyRjSZTNk"

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

print("البوت المتقدم والكامل يعمل الآن ✅")
app.run_polling()
