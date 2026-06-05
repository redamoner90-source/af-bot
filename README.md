# AF Bot - AppsFlyer Telegram Bot Manager

**بوت تلغرام متقدم لإدارة أحداث AppsFlyer مع دعم الجدولة التلقائية**

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-red)

---

## 📋 المميزات

✅ **إدارة متعددة المستخدمين** - كل مستخدم له أجهزة وإعدادات خاصة به
✅ **إرسال أحداث Level** - أحداث اللعبة المختلفة
✅ **إرسال أحداث Purchase** - أحداث الشراء مع المبالغ
✅ **جدولة تلقائية** - جدول الأحداث حسب الطلب
✅ **واجهة سهلة** - قوائم تفاعلية في Telegram
✅ **تخزين البيانات** - حفظ إعدادات المستخدمين والمهام المجدولة
✅ **دعم Proxy** - الاتصال عبر بروكسي SOCKS5

---

## 🚀 المتطلبات

- **Python 3.8 أو أعلى**
- **Telegram Bot Token** - من [@BotFather](https://t.me/botfather)
- **AppsFlyer Dev Key** - من حسابك في AppsFlyer
- **Internet Connection**

---

## 📦 التثبيت

### 1. نسخ المستودع
```bash
git clone https://github.com/redamoner90-source/af-bot.git
cd af-bot
```

### 2. تثبيت المكتبات
```bash
pip install -r requirements.txt
```

### 3. إعداد ملف التكوين
```bash
cp .env.example .env
```

ثم عدّل الملف وأضف:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
APPSFLYER_DEV_KEY=your_dev_key_here
```

### 4. تشغيل البوت
```bash
python telegram_bot.py
```

---

## 🎮 طريقة الاستخدام

### الأوامر الرئيسية

| الأمر | الوصف |
|------|-------|
| `/start` | بدء البوت |
| `/menu` | القائمة الرئيسية |
| `/settings` | إعدادات الجهاز (GAID, AF UID) |
| `/events` | إرسال أحداث |
| `/schedule` | جدولة أحداث |
| `/logs` | عرض السجلات |
| `/help` | المساعدة |

### خطوات الاستخدام

**1️⃣ إعداد الجهاز:**
- اضغط `/start`
- أضف GAID (Advertising ID)
- أضف AF UID (AppsFlyer ID)

**2️⃣ إرسال حدث:**
- اختر `/events`
- اختر نوع الحدث (Level أو Purchase)
- أدخل التفاصيل

**3️⃣ جدولة حدث:**
- اختر `/schedule`
- اختر الحدث
- حدد التكرار (مرة واحدة، يومياً، كل ساعة، إلخ)

---

## 📁 هيكل المشروع

```
af-bot/
├── README.md                    # هذا الملف
├── requirements.txt             # المكتبات المطلوبة
├── .env.example                # مثال على متغيرات البيئة
├── .gitignore                  # ملفات يتم تجاهلها
│
├── telegram_bot.py             # كود البوت الرئيسي
├── config.py                   # التكوينات والإعدادات
├── af_manager.py               # مدير AppsFlyer
├── user_manager.py             # مدير المستخدمين
├── scheduler.py                # نظام الجدولة
│
├── af_pusher.py                # السكريبت الأصلي
│
└── data/                        # مجلد البيانات (يُنشأ تلقائياً)
    ├── users.json              # بيانات المستخدمين
    ├── scheduled_tasks.json    # المهام المجدولة
    └── af_events.log           # سجل الأحداث
```

---

## ⚙️ متغيرات البيئة (.env)

```env
# Telegram Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_ADMIN_ID=your_admin_id_here

# AppsFlyer Configuration
APPSFLYER_DEV_KEY=your_dev_key_here

# Proxy Configuration (اختياري)
USE_PROXY=0
PROXY_IP_PORT=
PROXY_USERNAME=
PROXY_PASSWORD=

# Bot Settings
SHOW_RESPONSE=1
LOG_FILE=data/af_events.log
```

---

## 🔧 التطوير

### إضافة ميزة جديدة

1. عدّل الملف المناسب
2. أضف الاختبارات
3. اعمل Commit
4. اعمل Push

### أمثلة الكود

**إرسال حدث:**
```python
from af_manager import send_level_event

send_level_event(
    user_id="123456",
    event_name="af_level_up_5",
    app_id="com.example.game"
)
```

**جدولة حدث:**
```python
from scheduler import schedule_event

schedule_event(
    user_id="123456",
    event_type="purchase",
    amount=9.99,
    repeat="daily",
    time="10:00"
)
```

---

## 📝 السجلات

جميع الأحداث تُحفظ في `data/af_events.log`:

```
[2026-01-15 10:30:45] LEVEL | af_level_up_5 | Success | Status: 200
[2026-01-15 10:31:20] PURCHASE | af_purchase | 9.99 USD | Success | Status: 200
```

---

## 🐛 استكشاف الأخطاء

### المشكلة: البوت لا يستجيب
**الحل:** تحقق من:
- صحة `TELEGRAM_BOT_TOKEN`
- الاتصال بالإنترنت
- تشغيل البوت: `python telegram_bot.py`

### المشكلة: أحداث لا تُرسل
**الحل:** تحقق من:
- صحة `APPSFLYER_DEV_KEY`
- صحة GAID و AF UID
- السجلات: `/logs`

### المشكلة: الجدولة لا تعمل
**الحل:** تأكد من:
- الوقت بصيغة صحيحة (HH:MM)
- المنطقة الزمنية صحيحة

---

## 📞 الدعم والمساهمة

للإبلاغ عن مشكلة أو اقتراح ميزة:
- افتح **Issue** في GitHub
- أو تواصل مع المطور

---

## 📄 الترخيص

هذا المشروع مرخص تحت **MIT License**

---

## 👨‍💻 المطور

**TeamSR**
- Telegram: [@shohanur075](https://t.me/shohanur075)
- GitHub: [@redamoner90-source](https://github.com/redamoner90-source)

---

**آخر تحديث:** 2026-06-05
