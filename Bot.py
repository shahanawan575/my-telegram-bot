import telebot
from telebot import types

# 🔴 YAHAN APNA TOKEN AUR ADMIN ID LAZMI DALEIN 🔴
TOKEN = '8936519110:AAGbCzDi9zhQxW9-csJICM_c5yMX5yzwRuc'
ADMIN_ID = 7292874888

bot = telebot.TeleBot(TOKEN)

# ==========================================
# 1. PREMIUM WELCOME MESSAGE & BUTTON
# ==========================================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Agar admin /start kare
    if message.chat.id == ADMIN_ID:
        bot.send_message(ADMIN_ID, "👑 <b>Welcome Admin!</b> Bot is running perfectly.\n\nWait for user messages. Reply format:\n<code>/reply UserID Message</code>", parse_mode='HTML')
        return

    # Premium Button
    markup = types.InlineKeyboardMarkup()
    support_btn = types.InlineKeyboardButton("💬 Contact Support Team", callback_data='support_warning')
    markup.add(support_btn)
    
    # Premium Welcome Text
    welcome_text = (
        f"💎 <b>Welcome to USDT Mining Support</b> 💎\n\n"
        f"Hello <b>{message.from_user.first_name}</b>! 👋\n"
        f"Our premium support team is here to help you maximize your mining experience.\n\n"
        f"👇 <i>Click the button below to contact us.</i>"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode='HTML')

# ==========================================
# 2. PREMIUM WARNING MESSAGE (ON BUTTON CLICK)
# ==========================================
@bot.callback_query_handler(func=lambda call: call.data == 'support_warning')
def support_callback(call):
    warning_text = (
        "🛡️ <b>STRICT SUPPORT POLICY</b> 🛡️\n\n"
        "<i>Please read carefully before proceeding:</i>\n\n"
        "📌 We only assist with <b>USDT Mining Bot</b> related queries.\n"
        "🚫 <b>WARNING:</b> Any spam, promotional links, or irrelevant messages will result in an <b>INSTANT PERMANENT BAN</b> without notice.\n\n"
        "✍️ <i>If you agree, please type your message below and send it to us...</i>"
    )
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                          text=warning_text, parse_mode='HTML')

# ==========================================
# 3. ADMIN REPLY FUNCTION
# ==========================================
@bot.message_handler(commands=['reply'])
def admin_reply(message):
    if message.chat.id == ADMIN_ID:
        try:
            parts = message.text.split(' ', 2)
            user_id = parts[1]
            reply_text = parts[2]
            
            # User ko premium reply format
            user_reply = f"👨‍💻 <b>Support Team Reply:</b>\n\n<blockquote>{reply_text}</blockquote>\n\n<i>Thank you for using our USDT Mining service.</i>"
            bot.send_message(user_id, user_reply, parse_mode='HTML')
            
            # Admin ko success msg
            bot.reply_to(message, f"✅ <b>Message Successfully Sent!</b>\n👤 To ID: <code>{user_id}</code>", parse_mode='HTML')
        except Exception as e:
            bot.reply_to(message, "❌ <b>Error:</b> Incorrect format.\n\nUse: <code>/reply UserID Your message here</code>", parse_mode='HTML')

# ==========================================
# 4. HANDLE USER MESSAGE & SEND TO ADMIN
# ==========================================
@bot.message_handler(func=lambda message: message.chat.id != ADMIN_ID)
def handle_user_message(message):
    
    # 🌟 ADMIN KO PREMIUM MESSAGE RECEIVE HOGA 🌟
    user_info = (
        "🚨 <b>NEW SUPPORT TICKET</b> 🚨\n\n"
        f"👤 <b>User:</b> {message.from_user.first_name}\n"
        f"🆔 <b>ID:</b> <code>{message.chat.id}</code> (Tap to copy)\n"
        f"🔗 <b>Username:</b> @{message.from_user.username if message.from_user.username else 'No Username'}\n\n"
        f"💬 <b>Message:</b>\n<blockquote>{message.text}</blockquote>\n\n"
        f"📝 <b>Reply Command:</b>\n<code>/reply {message.chat.id} Type your answer here</code>"
    )
    
    try:
        # Send to Admin
        bot.send_message(ADMIN_ID, user_info, parse_mode='HTML')
        
        # Acknowledge User
        bot.reply_to(message, "✅ <b>Message Received!</b>\n\nOur support team will review your USDT mining query and get back to you shortly.", parse_mode='HTML')
        print(f"Message forwarded to admin from {message.from_user.first_name}")
    except Exception as e:
        print(f"Admin ko message bhejte waqt error: {e}")
        # Agar admin ID galat hogi to terminal me error dikhega

print("💎 Premium Bot is Running...")
bot.polling(none_stop=True)
          
