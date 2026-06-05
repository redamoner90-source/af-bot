# 🚀 خطوات التثبيت والتشغيل

## المتطلبات
- Python 3.8+
- pip (مدير الحزم)
- Telegram Bot Token
- AppsFlyer Dev Key

## خطوات التثبيت

### 1. نسخ المستودع
```bash
git clone https://github.com/redamoner90-source/af-bot.git
cd af-bot
```

### 2. إنشاء بيئة افتراضية (اختياري لكن موصى به)
```bash
python -m venv venv

# على Windows:
venv\Scripts\activate

# على Linux/Mac:
source venv/bin/activate
```

### 3. تثبيت المكتبات
```bash
pip install -r requirements.txt
```

### 4. إعداد ملف البيئة
```bash
# انسخ الملف النموذجي
cp .env.example .env

# عدّل الملف وأضف:
# TELEGRAM_BOT_TOKEN=your_token_here
# APPSFLYER_DEV_KEY=your_key_here
```

### 5. الحصول على البيانات المطلوبة

**Telegram Bot Token:**
- اذهب إلى [@BotFather](https://t.me/botfather) على Telegram
- أرسل `/newbot`
- اتبع التعليمات
- انسخ Token

**AppsFlyer Dev Key:**
- اذهب إلى [AppsFlyer Dashboard](https://www.appsflyer.com/)
- اذهب إلى Settings → Dev Key
- انسخ المفتاح

### 6. تشغيل البوت
```bash
python telegram_bot.py
```

## ✅ التحقق من التشغيل
إذا رأيت:
```
🚀 Bot is running...
```

هذا يعني أن البوت يعمل بنجاح!

## 🔧 حل المشاكل الشائعة

### خطأ: ModuleNotFoundError
**الحل:** تأكد من تثبيت جميع المكتبات:
```bash
pip install -r requirements.txt
```

### خطأ: .env file not found
**الحل:** أنشئ ملف .env:
```bash
cp .env.example .env
```

### البوت لا يستجيب
**الحل:** تحقق من:
1. صحة TELEGRAM_BOT_TOKEN
2. الاتصال بالإنترنت
3. البوت يعمل في terminal

## 📞 الدعم
إذا واجهت أي مشاكل، افتح Issue على GitHub!
