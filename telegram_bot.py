#!/usr/bin/env python3
"""
AF Bot - Main Telegram Bot for AppsFlyer Event Management
"""

import os
import uuid
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    ConversationHandler, filters, ContextTypes
)

from config import (
    TELEGRAM_BOT_TOKEN, APPSFLYER_DEV_KEY, DEFAULT_CURRENCY, 
    PRESET_AMOUNTS, LOG_FILE
)
from af_manager import AFManager
from user_manager import UserManager
from scheduler import TaskScheduler

# Initialize managers
user_manager = UserManager()
af_manager = AFManager(APPSFLYER_DEV_KEY)
task_scheduler = TaskScheduler()

# Conversation states
SELECTING_ACTION, DEVICE_SETUP, SEND_LEVEL, SEND_PURCHASE, SCHEDULE_EVENT = range(5)

def log_event(event_text: str):
    """Log events to file"""
    Path(LOG_FILE).parent.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {event_text}\n")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command"""
    user_id = str(update.effective_user.id)
    username = update.effective_user.username or "User"
    
    user_manager.add_user(user_id, username)
    
    welcome_text = f"""
🚀 **مرحباً {username}!**

أهلاً وسهلاً في AF Bot

هذا البوت يساعدك على إدارة أحداث AppsFlyer بسهولة!

اختر من القائمة أدناه:
"""
    
    keyboard = [
        [InlineKeyboardButton("📱 إضافة جهاز", callback_data="add_device")],
        [InlineKeyboardButton("📤 إرسال حدث", callback_data="send_event")],
        [InlineKeyboardButton("⏰ جدولة حدث", callback_data="schedule_event")],
        [InlineKeyboardButton("⚙️ الإعدادات", callback_data="settings")],
        [InlineKeyboardButton("📋 المساعدة", callback_data="help")]
    ]
    
    await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    log_event(f"User {user_id} ({username}) started the bot")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button presses"""
    query = update.callback_query
    user_id = str(query.from_user.id)
    
    await query.answer()
    
    if query.data == "add_device":
        await query.edit_message_text(
            text="📱 **إضافة جهاز جديد**\n\nأدخل GAID (Advertising ID):",
            parse_mode="Markdown"
        )
        context.user_data['action'] = 'add_device'
        return DEVICE_SETUP
    
    elif query.data == "send_event":
        keyboard = [
            [InlineKeyboardButton("⬆️ حدث Level", callback_data="event_level")],
            [InlineKeyboardButton("💰 حدث Purchase", callback_data="event_purchase")],
            [InlineKeyboardButton("🔙 رجوع", callback_data="back")]
        ]
        await query.edit_message_text(
            text="📤 **اختر نوع الحدث:**",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
    
    elif query.data == "event_level":
        devices = user_manager.get_devices(user_id)
        if not devices:
            await query.edit_message_text("❌ لم تضف أي أجهزة! أضف جهاز أولاً.")
            return
        
        context.user_data['action'] = 'send_level'
        context.user_data['device_index'] = 0
        
        keyboard = [[InlineKeyboardButton(f"Device {i+1}", callback_data=f"device_{i}")] 
                   for i in range(len(devices))]
        keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="back")])
        
        await query.edit_message_text(
            text="📱 **اختر الجهاز:**",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
    
    elif query.data == "event_purchase":
        devices = user_manager.get_devices(user_id)
        if not devices:
            await query.edit_message_text("❌ لم تضف أي أجهزة! أضف جهاز أولاً.")
            return
        
        context.user_data['action'] = 'send_purchase'
        context.user_data['device_index'] = 0
        
        keyboard = [[InlineKeyboardButton(f"Device {i+1}", callback_data=f"device_{i}")] 
                   for i in range(len(devices))]
        keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="back")])
        
        await query.edit_message_text(
            text="📱 **اختر الجهاز:**",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
    
    elif query.data.startswith("device_"):
        device_index = int(query.data.split("_")[1])
        context.user_data['device_index'] = device_index
        
        action = context.user_data.get('action')
        
        if action == "send_level":
            await query.edit_message_text(
                text="🎮 **أدخل اسم الحدث:**\n\nمثلاً: af_level_up_5",
                parse_mode="Markdown"
            )
            context.user_data['awaiting_event_name'] = True
        
        elif action == "send_purchase":
            keyboard = [
                [InlineKeyboardButton(f"${amt:.2f}", callback_data=f"amount_{amt}")] 
                for amt in PRESET_AMOUNTS[:3]
            ]
            keyboard.append([InlineKeyboardButton(f"${PRESET_AMOUNTS[3]:.2f}", callback_data=f"amount_{PRESET_AMOUNTS[3]}")])
            keyboard.append([InlineKeyboardButton(f"${PRESET_AMOUNTS[4]:.2f}", callback_data=f"amount_{PRESET_AMOUNTS[4]}")])
            keyboard.append([InlineKeyboardButton(f"${PRESET_AMOUNTS[5]:.2f}", callback_data=f"amount_{PRESET_AMOUNTS[5]}")])
            keyboard.append([InlineKeyboardButton(f"${PRESET_AMOUNTS[6]:.2f}", callback_data=f"amount_{PRESET_AMOUNTS[6]}")])
            keyboard.append([InlineKeyboardButton("💵 مبلغ مخصص", callback_data="custom_amount")])
            keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="back")])
            
            await query.edit_message_text(
                text="💰 **اختر المبلغ:**",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="Markdown"
            )
    
    elif query.data.startswith("amount_"):
        try:
            amount = float(query.data.split("_")[1])
            user_id = str(query.from_user.id)
            device_index = context.user_data.get('device_index', 0)
            devices = user_manager.get_devices(user_id)
            
            if device_index >= len(devices):
                await query.answer("❌ خطأ في اختيار الجهاز")
                return
            
            device = devices[device_index]
            result = af_manager.send_purchase_event(
                device['af_uid'],
                device['gaid'],
                device['app_id'],
                amount,
                DEFAULT_CURRENCY
            )
            
            if result['success']:
                await query.edit_message_text(
                    f"✅ تم إرسال الحدث بنجاح!\n\n💰 {amount} {DEFAULT_CURRENCY}",
                    parse_mode="Markdown"
                )
                log_event(f"User {user_id} sent purchase event: {amount} {DEFAULT_CURRENCY}")
            else:
                await query.edit_message_text("❌ فشل إرسال الحدث!")
        except Exception as e:
            await query.edit_message_text(f"❌ خطأ: {str(e)}")
    
    elif query.data == "custom_amount":
        await query.edit_message_text(
            text="💵 **أدخل المبلغ:**\n\nمثلاً: 5.99",
            parse_mode="Markdown"
        )
        context.user_data['awaiting_amount'] = True
    
    elif query.data == "schedule_event":
        await query.edit_message_text(
            text="⏰ **جدولة حدث جديد**\n\nهذه الميزة قيد التطوير!",
            parse_mode="Markdown"
        )
    
    elif query.data == "settings":
        devices = user_manager.get_devices(user_id)
        devices_text = "\n".join([f"📱 Device {i+1}: {d['gaid'][:10]}..." 
                                 for i, d in enumerate(devices)]) or "لا توجد أجهزة"
        
        await query.edit_message_text(
            text=f"⚙️ **الإعدادات**\n\n{devices_text}",
            parse_mode="Markdown"
        )
    
    elif query.data == "help":
        help_text = """
📚 **المساعدة**

**إرسال حدث:**
اختر الحدث (Level أو Purchase) وأدخل التفاصيل

**جدولة حدث:**
اختر الحدث والتكرار والوقت

**الإعدادات:**
أضف أو عدّل GAID و AF UID

**السجلات:**
اعرض آخر الأحداث المرسلة
"""
        await query.edit_message_text(help_text, parse_mode="Markdown")
    
    elif query.data == "back":
        await start(update, context)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages"""
    user_id = str(update.effective_user.id)
    text = update.message.text
    
    if context.user_data.get('action') == 'add_device' and not context.user_data.get('gaid_set'):
        context.user_data['gaid'] = text
        context.user_data['gaid_set'] = True
        await update.message.reply_text("✅ تم حفظ GAID\n\nالآن أدخل AF UID:")
    
    elif context.user_data.get('action') == 'add_device' and context.user_data.get('gaid_set') and not context.user_data.get('afuid_set'):
        context.user_data['af_uid'] = text
        context.user_data['afuid_set'] = True
        await update.message.reply_text("✅ تم حفظ AF UID\n\nالآن أدخل App ID:")
    
    elif context.user_data.get('action') == 'add_device' and context.user_data.get('afuid_set') and not context.user_data.get('appid_set'):
        context.user_data['app_id'] = text
        
        user_manager.add_device(
            user_id,
            context.user_data['gaid'],
            context.user_data['af_uid'],
            context.user_data['app_id']
        )
        
        await update.message.reply_text("✅ تم إضافة الجهاز بنجاح!")
        log_event(f"User {user_id} added new device")
        
        context.user_data.clear()
        await start(update, context)
    
    elif context.user_data.get('awaiting_event_name'):
        device_index = context.user_data.get('device_index', 0)
        devices = user_manager.get_devices(user_id)
        device = devices[device_index]
        
        result = af_manager.send_level_event(
            device['af_uid'],
            device['gaid'],
            text,
            device['app_id']
        )
        
        if result['success']:
            await update.message.reply_text(f"✅ تم إرسال الحدث: {text}")
            log_event(f"User {user_id} sent level event: {text}")
        else:
            await update.message.reply_text("❌ فشل إرسال الحدث!")
        
        context.user_data.clear()
        await start(update, context)
    
    elif context.user_data.get('awaiting_amount'):
        try:
            amount = float(text)
            device_index = context.user_data.get('device_index', 0)
            devices = user_manager.get_devices(user_id)
            device = devices[device_index]
            
            result = af_manager.send_purchase_event(
                device['af_uid'],
                device['gaid'],
                device['app_id'],
                amount,
                DEFAULT_CURRENCY
            )
            
            if result['success']:
                await update.message.reply_text(f"✅ تم إرسال الحدث بنجاح!\n\n💰 {amount} {DEFAULT_CURRENCY}")
                log_event(f"User {user_id} sent purchase event: {amount} {DEFAULT_CURRENCY}")
            else:
                await update.message.reply_text("❌ فشل إرسال الحدث!")
        except ValueError:
            await update.message.reply_text("❌ الرجاء إدخال مبلغ صحيح (رقم)")
        
        context.user_data.clear()
        await start(update, context)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    print(f"Error: {context.error}")

def main():
    """Main function"""
    # Ensure .env exists
    if not Path('.env').exists():
        print("❌ Error: .env file not found!")
        print("Please create .env file with TELEGRAM_BOT_TOKEN and APPSFLYER_DEV_KEY")
        return
    
    # Create application
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)
    
    # Start scheduler
    task_scheduler.start()
    
    print("🚀 Bot is running...")
    log_event("Bot started")
    
    # Run bot
    app.run_polling()

if __name__ == "__main__":
    main()
