import logging
import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# إعدادات البوت
TOKEN = "8143737130:AAFdSpl_EQuHjHHIjr2eE4y5MDfxtQvrtxg"  # ضع توكن البوت هنا
OWNER_ID = 6735264173  # أيدي صاحب البوت
admins = [OWNER_ID]  # إضافة الأورنر الأول هنا

# بيانات المستخدمين
user_data = {}
user_ids = set()  # لتخزين الأيدي
user_count = 1  # عدد الأعضاء
banned_users = set()  # لتخزين الأعضاء المحظورين

# حالات المحادثة للتسجيل
EMAIL, PASSWORD, REGISTERED = range(3)

# قائمة الإيميلات وكلمات المرور المسموح بها
allowed_emails = [
    "qroom3452@qro.com", "qroom8763@qro.com", "qroom4951@qro.com", "qroom2378@qro.com",
    "qroom6492@qro.com", "qroom5843@qro.com", "qroom7635@qro.com", "qroom2917@qro.com",
    "qroom1284@qro.com", "qroom4172@qro.com", "qroom9305@qro.com", "qroom8567@qro.com",
    "qroom1024@qro.com", "qroom7531@qro.com", "qroom6842@qro.com", "qroom2398@qro.com",
    "qroom3706@qro.com", "qroom5809@qro.com", "qroom9471@qro.com", "qroom4153@qro.com",
    "qroom7260@qro.com", "qroom3157@qro.com", "qroom5902@qro.com", "qroom8614@qro.com",
    "qroom2048@qro.com", "qroom6731@qro.com", "qroom5084@qro.com", "qroom7625@qro.com",
    "qroom4183@qro.com", "qroom2395@qro.com", "qroomrakan@gmail.com"  # إضافة إيميل الأورنر
]
# كلمات المرور المقابلة للإيميلات (بنفس الترتيب)
allowed_passwords = [
    "Qroom238yJd", "Qroom103aXp", "Qroom562tLv", "Qroom491rNz",
    "Qroom813sQm", "Qroom324uBk", "Qroom110dWp", "Qroom871xJv",
    "Qroom543mHf", "Qroom934zLc", "Qroom274oVd", "Qroom642wXb",
    "Qroom839jWp", "Qroom203aFy", "Qroom520tGc", "Qroom154kBx",
    "Qroom947vDp", "Qroom680zLv", "Qroom128nHv", "Qroom593qJd",
    "Qroom482pKf", "Qroom653rWy", "Qroom472dZv", "Qroom928aQj",
    "Qroom415tNr", "Qroom569sXm", "Qroom760jTb", "Qroom213wQk",
    "Qroom985vHl", "Qroom736zBq", "Messi_100"  # إضافة كلمة مرور الأورنر
]

# قاموس لتخزين الإيميلات المستخدمة
used_emails = {}  # {email: user_id}

# تفعيل تسجيل الأخطاء
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# عند بدء المحادثة
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # إذا كان من الأورنر، اسمح له بالدخول مباشرة
    if user.id in admins:
        await admin_start(update, context)
        return ConversationHandler.END

    # إذا تم تسجيل المستخدم مسبقاً
    if user.id in user_data and user_data[user.id].get('is_registered', False):
        await show_welcome(update, context)
        return ConversationHandler.END

    # طلب البريد الإلكتروني
    start_message = await update.message.reply_text(
        "🔹 أرسل البريد الإلكتروني الخاص بك.\n\n"
        "إذا لم يكن لديك بريد إلكتروني وكلمة مرور، توجه إلى الموقع لشرائهما: https://qroom.netlify.app/"
    )

    # حفظ معرف رسالة الترحيب لاستخدامها لاحقًا
    context.user_data['start_message_id'] = start_message.message_id

    return EMAIL

# معالجة البريد الإلكتروني
async def email_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    email = update.message.text.strip().lower()
    user_id = update.effective_user.id

    # حفظ معرف رسالة البريد الإلكتروني لحذفها لاحقًا
    context.user_data['email_message_id'] = update.message.message_id

    # التحقق من صحة البريد الإلكتروني
    if email not in allowed_emails:
        reply_message = await update.message.reply_text(
            "❌ البريد الإلكتروني غير صحيح.\n"
            "لشراء بريد إلكتروني وكلمة مرور توجه للشراء من الموقع: https://qroom.netlify.app/"
        )
        return EMAIL

    # التحقق مما إذا كان البريد مستخدماً بالفعل
    if email in used_emails and used_emails[email] != user_id:
        reply_message = await update.message.reply_text(
            "❌ هذا البريد الإلكتروني مستخدم بالفعل.\n"
            "لشراء بريد إلكتروني وكلمة مرور توجه للشراء من الموقع: https://qroom.netlify.app/"
        )
        return EMAIL

    # تخزين البريد الإلكتروني مؤقتاً في سياق المحادثة
    context.user_data['email'] = email

    # طلب كلمة المرور
    password_message = await update.message.reply_text("🔹 أرسل كلمة المرور:")

    # حفظ معرف رسالة طلب كلمة المرور
    context.user_data['password_prompt_id'] = password_message.message_id

    return PASSWORD

# معالجة كلمة المرور
async def password_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    password = update.message.text.strip()
    email = context.user_data.get('email', '')
    user = update.effective_user

    # حفظ معرف رسالة كلمة المرور لحذفها لاحقًا
    context.user_data['password_message_id'] = update.message.message_id

    # التحقق من صحة البريد الإلكتروني وكلمة المرور
    if email in allowed_emails:
        email_index = allowed_emails.index(email)
        correct_password = allowed_passwords[email_index]

        if password == correct_password:
            # تسجيل المستخدم
            global user_count  # استخدام المتغير global هنا

            if user.id not in user_data:
                user_data[user.id] = {
                    'username': user.username,
                    'member_number': user_count,
                    'id': user.id,
                    'email': email,
                    'is_registered': True,
                    'search_history': []
                }
                user_count += 1
                user_ids.add(user.id)
            else:
                user_data[user.id]['email'] = email
                user_data[user.id]['is_registered'] = True

            # تسجيل البريد الإلكتروني كمستخدم
            used_emails[email] = user.id

            # حذف رسائل البريد الإلكتروني وكلمة المرور
            try:
                # حذف رسالة البريد الإلكتروني
                await context.bot.delete_message(
                    chat_id=update.effective_chat.id,
                    message_id=context.user_data.get('email_message_id')
                )

                # حذف رسالة طلب كلمة المرور
                await context.bot.delete_message(
                    chat_id=update.effective_chat.id,
                    message_id=context.user_data.get('password_prompt_id')
                )

                # حذف رسالة كلمة المرور
                await context.bot.delete_message(
                    chat_id=update.effective_chat.id,
                    message_id=context.user_data.get('password_message_id')
                )

                # حذف رسالة البداية
                if 'start_message_id' in context.user_data:
                    await context.bot.delete_message(
                        chat_id=update.effective_chat.id,
                        message_id=context.user_data.get('start_message_id')
                    )
            except Exception as e:
                logging.error(f"خطأ في حذف الرسائل: {str(e)}")

            success_message = await update.message.reply_text("✅ تم تسجيل الدخول بنجاح! أرسل أمر /start")

            # إرسال إشعار للأورنر بالتسجيل الجديد
            for admin_id in admins:
                registration_info = (
                    f"📝 **تسجيل جديد:**\n"
                    f"👤 **الاسم:** {user.full_name}\n"
                    f"🔹 **المعرف:** @{user.username if user.username else 'لا يوجد'}\n"
                    f"🆔 **الأيدي:** {user.id}\n"
                    f"📧 **البريد الإلكتروني:** {email}\n"
                    f"⏳ **وقت التسجيل:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"🔢 **رقم العضوية:** {user_data[user.id]['member_number']}"
                )
                await context.bot.send_message(chat_id=admin_id, text=registration_info, parse_mode="Markdown")

            return ConversationHandler.END
        else:
            await update.message.reply_text("❌ كلمة المرور غير صحيحة، حاول مرة أخرى.")
            return PASSWORD
    else:
        await update.message.reply_text(
            "❌ البريد الإلكتروني غير صحيح.\n"
            "لشراء بريد إلكتروني وكلمة مرور توجه للشراء من الموقع: https://qroom.netlify.app/"
        )
        return EMAIL

# عرض رسالة الترحيب للمستخدمين المسجلين
async def show_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_message = f"🔹 منور بوت Qroom Movies 🤩💙\n\n🔹 اكتب اسم فلمك او مسلسلك\n\nرقم عضويتك هو: {user_data[user.id]['member_number']}"
    await update.message.reply_text(welcome_message)

# الترحيب بالأورنر
async def admin_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global user_count  # استخدام المتغير global هنا
    user = update.effective_user

    # إضافة المستخدم إذا كان جديدًا
    if user.id not in user_data:
        user_data[user.id] = {
            'username': user.username,
            'member_number': user_count,
            'id': user.id,
            'is_registered': True,  # الأورنر مسجل تلقائيًا
            'search_history': []
        }
        user_count += 1
        user_ids.add(user.id)

    welcome_message = f"🔹 مرحباً بك أيها الأورنر في بوت Qroom Movies 🤩💙\n\n🔹 اكتب اسم فلمك او مسلسلك\n\nرقم عضويتك هو: {user_data[user.id]['member_number']}"
    await update.message.reply_text(welcome_message)

# البحث عن فيلم أو مسلسل
async def search_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # التحقق من تسجيل المستخدم
    if user.id not in user_data or not user_data[user.id].get('is_registered', False):
        if user.id not in admins:  # إذا لم يكن أورنر
            await update.message.reply_text(
                "⚠️ يجب عليك التسجيل أولاً. أرسل /start للبدء."
            )
            return

    # التحقق من الحظر
    if user.id in banned_users:
        await update.message.reply_text("🚫 لقد تم حظرك من استخدام هذا البوت.")
        return

    movie_name = update.message.text.strip()

    if movie_name:
        search_url = f"https://shah4u.net/search?s={movie_name.replace(' ', '+')}"

        # إرسال النتيجة للمستخدم كرابط مخفي
        await update.message.reply_text(f"اضغط هنا 👈🏻 : [{movie_name}]({search_url})", parse_mode="Markdown", disable_web_page_preview=True)

        # إرسال تقرير البحث إلى صاحب البوت
        search_info = (
            f"🔍 **بحث جديد:**\n"
            f"👤 **الاسم:** {user.full_name}\n"
            f"🔹 **المعرف:** @{user.username if user.username else 'لا يوجد'}\n"
            f"🆔 **الأيدي:** {user.id}\n"
            f"🎬 **البحث عن:** {movie_name}\n"
            f"⏳ **وقت البحث:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

        for admin_id in admins:
            await context.bot.send_message(chat_id=admin_id, text=search_info, parse_mode="Markdown")

    else:
        await update.message.reply_text("من فضلك ادخل اسم فيلم أو مسلسل")

# إلغاء المحادثة
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("تم إلغاء العملية. أرسل /start للبدء من جديد.")
    return ConversationHandler.END

# حظر المستخدم
async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id not in admins:
        await update.message.reply_text("❌ هذا الأمر مخصص للأورنر فقط.")
        return

    if context.args:
        try:
            user_id = int(context.args[0])
            banned_users.add(user_id)
            await update.message.reply_text(f"✅ تم حظر المستخدم {user_id}")
        except ValueError:
            await update.message.reply_text("❌ يرجى إدخال أيدي صالح.")
    else:
        await update.message.reply_text("❌ استخدم الأمر كالتالي: `/ban user_id`", parse_mode="Markdown")

# إلغاء حظر المستخدم
async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id not in admins:
        await update.message.reply_text("❌ هذا الأمر مخصص للأورنر فقط.")
        return

    if context.args:
        try:
            user_id = int(context.args[0])
            if user_id in banned_users:
                banned_users.remove(user_id)
                await update.message.reply_text(f"✅ تم إلغاء حظر المستخدم {user_id}")
            else:
                await update.message.reply_text("❌ هذا المستخدم غير محظور.")
        except ValueError:
            await update.message.reply_text("❌ يرجى إدخال أيدي صالح.")
    else:
        await update.message.reply_text("❌ استخدم الأمر كالتالي: `/unban user_id`", parse_mode="Markdown")

# عرض الأعضاء المحظورين
async def banded(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in admins:
        await update.message.reply_text("❌ هذا الأمر مخصص للأورنر فقط.")
        return

    banned_list = "\n".join(str(user_id) for user_id in banned_users)
    if banned_list:
        await update.message.reply_text(f"الأعضاء المحظورين:\n{banned_list}")
    else:
        await update.message.reply_text("لا يوجد أعضاء محظورين حالياً.")

# إضافة أورنر جديد
async def add_owner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id not in admins:
        await update.message.reply_text("❌ هذا الأمر مخصص للأورنر فقط.")
        return

    if context.args:
        try:
            new_owner_id = int(context.args[0])
            admins.append(new_owner_id)
            await update.message.reply_text(f"✅ تم إضافة الأورنر {new_owner_id}")
        except ValueError:
            await update.message.reply_text("❌ يرجى إدخال أيدي صالح.")
    else:
        await update.message.reply_text("❌ استخدم الأمر كالتالي: `/owner <user_id>`", parse_mode="Markdown")

# حذف أورنر إضافي
async def remove_owner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id != OWNER_ID:
        await update.message.reply_text("❌ هذا الأمر مخصص لصاحب البوت فقط.")
        return

    if context.args:
        try:
            remove_owner_id = int(context.args[0])
            if remove_owner_id in admins and remove_owner_id != OWNER_ID:
                admins.remove(remove_owner_id)
                await update.message.reply_text(f"✅ تم إزالة الأورنر {remove_owner_id}")
            else:
                await update.message.reply_text("❌ هذا الشخص ليس أورنر أو هو صاحب البوت.")
        except ValueError:
            await update.message.reply_text("❌ يرجى إدخال أيدي صالح.")
    else:
        await update.message.reply_text("❌ استخدم الأمر كالتالي: `/ownerend <user_id>`", parse_mode="Markdown")

# عرض جميع أوامر البوت
async def show_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands = (
        "/start - بدء البوت\n"
        "/ban <user_id> - حظر المستخدم\n"
        "/unban <user_id> - إلغاء حظر المستخدم\n"
        "/banded - عرض الأعضاء المحظورين\n"
        "/owner <user_id> - إضافة أورنر جديد\n"
        "/ownerend <user_id> - حذف أورنر إضافي\n"
    )
    await update.message.reply_text(f"📜 **أوامر البوت:**\n\n{commands}")

# تشغيل البوت
def main():
    app = Application.builder().token(TOKEN).build()

    # محادثة التسجيل
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, email_step)],
            PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, password_step)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv_handler)

    # أوامر البوت
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_movie))
    app.add_handler(CommandHandler("ban", ban_user))
    app.add_handler(CommandHandler("unban", unban_user))
    app.add_handler(CommandHandler("banded", banded))  # عرض الأعضاء المحظورين
    app.add_handler(CommandHandler("owner", add_owner))  # إضافة أورنر جديد
    app.add_handler(CommandHandler("ownerend", remove_owner))  # حذف أورنر إضافي
    app.add_handler(CommandHandler("bots", show_commands))  # عرض جميع أوامر البوت

    # تشغيل البوت
    print("✅ البوت يعمل الآن...")
    app.run_polling()

if __name__ == "__main__":
    main()
