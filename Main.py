import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)

# 🔐 Config
MAIN_ADMIN_ID = int(os.getenv("MAIN_ADMIN_ID", "123456789"))  # beddel default
ALLOWED_ADMINS = {MAIN_ADMIN_ID}
USERS = set()

# 📜 Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 🧾 Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    USERS.add(user_id)
    await update.message.reply_text("👋 Welcome to the bot! Use /help for more.")

# 🆘 Help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Start the bot\n"
        "/help - Show help\n"
        "/profile - View your info\n"
        "/admin - Check admin access\n"
        "/addadmin <id> - Add a new admin (Main only)\n"
        "/broadcast <text> - Send message to all users"
    )

# 🧑 Profile
async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"🆔 ID: {user.id}\n👤 Username: @{user.username}"
    )

# 👑 Admin check
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in ALLOWED_ADMINS:
        await update.message.reply_text("✅ You are an admin.")
    else:
        await update.message.reply_text("⛔ You are NOT an admin.")

# ➕ Add admin
async def add_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != MAIN_ADMIN_ID:
        return await update.message.reply_text("⛔ Only main admin can add others.")
    try:
        new_admin_id = int(context.args[0])
        ALLOWED_ADMINS.add(new_admin_id)
        await update.message.reply_text(f"✅ Added new admin: {new_admin_id}")
    except:
        await update.message.reply_text("⚠️ Use like: /addadmin 123456789")

# 📣 Broadcast
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ALLOWED_ADMINS:
        return await update.message.reply_text("⛔ You are not allowed.")
    if not context.args:
        return await update.message.reply_text("⚠️ Use like: /broadcast Hello all!")
    text = " ".join(context.args)
    for uid in USERS:
        try:
            await context.bot.send_message(chat_id=uid, text=f"📢 {text}")
        except:
            continue
    await update.message.reply_text("📨 Broadcast sent!")

# 🚀 Main
def main():
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        print("❌ BOT_TOKEN not found in ENV")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("profile", profile))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(CommandHandler("addadmin", add_admin))
    app.add_handler(CommandHandler("broadcast", broadcast))

    app.run_polling()

if __name__ == '__main__':
    main()
