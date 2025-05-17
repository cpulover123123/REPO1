from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

import os
TOKEN = os.getenv('TOKEN')

# --- Main Menu Keyboard ---
def get_main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Deposit", callback_data='deposit'), InlineKeyboardButton("Withdraw", callback_data='withdraw')],
        [InlineKeyboardButton("🤖 AI CopyTrade", callback_data='ai_copytrade')],
        [InlineKeyboardButton("⚙ Settings", callback_data='settings')],
        [InlineKeyboardButton("📞 Contact Us", callback_data='contact')],
        [InlineKeyboardButton("🔄 Refresh", callback_data='refresh')]
    ])

# --- Back Button Keyboard ---
def get_back_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data='back')]
    ])

# --- /start Command and Refresh Handler ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = get_main_keyboard()
    message = (
        "Welcome to UraniumAI ,\nFastest & Securest World Wide.\n\n"
        "*Balance ≈ 0 SOL ($0.00)*\n"
        "`8GTayzAmuXrMJix1Cv72SE4m7TUrf3VoRDC3Fhg4oWZo` (tap to copy)\n\n"
        "*Deposit 1 SOL to begin AI CopyTrade*\n\n"
        "You currently have 0 holdings. To start trading, please deposit funds."
    )

    if update.message:
        await update.message.reply_text(message, parse_mode='Markdown', reply_markup=keyboard)
    elif update.callback_query:
        await update.callback_query.edit_message_text(message, parse_mode='Markdown', reply_markup=keyboard)

# --- Button Handler for Menu Navigation ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    responses = {
        "deposit": (
            "Fund your wallet using Solana.\n\n"
            "`8GTayzAmuXrMJix1Cv72SE4m7TUrf3VoRDC3Fhg4oWZo` (tap to copy)\n\n"
            "Deposit minimum 1 SOL to begin AI\n\n"
            "To deposit funds into your account, simply transfer funds from your wallet or exchange "
            "(such as Phantom, Coinbase, or any other supported platform)."
        ),
        "withdraw": "You must have funds to withdraw.",
        "ai_copytrade": "AI CopyTrade requires 1 SOL minimum.",
        "settings": "Settings locked until AI is active.",
        "contact": "Contact us at support.uraniumai@gmail.com",
    }

    if data in ["back", "refresh"]:
        await start(update, context)
    elif data in responses:
        await query.edit_message_text(
            text=responses[data],
            parse_mode='Markdown',
            reply_markup=get_back_keyboard()
        )
    else:
        await query.edit_message_text(
            text="Unknown action.",
            reply_markup=get_back_keyboard()
        )

# --- Main Function ---
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

if __name__ == "__main__":
    main()


