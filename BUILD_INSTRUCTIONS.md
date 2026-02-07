# 🔨 تعليمات البناء المفصلة

## المرحلة 1: التحضير

### 1.1 التحقق من المتطلبات
```bash
# التحقق من Java
java -version
# يجب أن تكون 11 أو أعلى

# التحقق من Gradle
gradle -version
# يجب أن تكون 8.0 أو أعلى

# التحقق من Android SDK
android list sdk
```

### 1.2 تعيين متغيرات البيئة
```bash
# على Linux/Mac
export ANDROID_HOME=/path/to/android/sdk
export JAVA_HOME=/path/to/java

# على Windows
set ANDROID_HOME=C:\path\to\android\sdk
set JAVA_HOME=C:\path\to\java
```

---

## المرحلة 2: تحميل Llama 3.5

### 2.1 تحميل النموذج من Hugging Face
```bash
# الطريقة 1: استخدام git-lfs
git lfs install
git clone https://huggingface.co/meta-llama/Llama-3.5-70B
mv Llama-3.5-70B llama3.5/models/

# الطريقة 2: استخدام Python
python3 scripts/download_llama.py

# الطريقة 3: تحميل يدوي
# 1. اذهب إلى https://huggingface.co/meta-llama/Llama-3.5-70B
# 2. اضغط Download
# 3. انقل الملفات إلى llama3.5/models/
```

### 2.2 التحقق من التحميل
```bash
ls -lah llama3.5/models/
# يجب أن ترى:
# - config.json
# - model.safetensors (13GB+)
# - tokenizer.json
# - special_tokens_map.json
```

---

## المرحلة 3: بناء التطبيق

### 3.1 تنظيف المشروع
```bash
cd /path/to/AIDeepinApp-Final-Complete
./gradlew clean
```

### 3.2 مزامنة Gradle
```bash
./gradlew sync
# أو في Android Studio: File > Sync Now
```

### 3.3 بناء Debug APK
```bash
./gradlew assembleDebug
# سيتم إنشاء:
# app/build/outputs/apk/debug/app-debug.apk
```

### 3.4 بناء Release APK
```bash
./gradlew assembleRelease
# سيتم إنشاء:
# app/build/outputs/apk/release/app-release.apk
```

### 3.5 بناء مع ProGuard
```bash
./gradlew assembleRelease -Pproguard=true
```

---

## المرحلة 4: التثبيت على الهاتف

### 4.1 التثبيت عبر ADB
```bash
# تأكد من توصيل الهاتف
adb devices

# تثبيت Debug APK
adb install app/build/outputs/apk/debug/app-debug.apk

# أو تثبيت Release APK
adb install app/build/outputs/apk/release/app-release.apk
```

### 4.2 التثبيت عبر Android Studio
1. افتح Android Studio
2. اختر Run > Run 'app'
3. اختر جهازك من القائمة
4. اضغط OK

### 4.3 التثبيت اليدوي
1. انقل ملف APK إلى الهاتف
2. افتح مدير الملفات
3. انقر على ملف APK
4. اضغط تثبيت

---

## المرحلة 5: التحقق من التثبيت

### 5.1 التحقق من التطبيق
```bash
# التحقق من تثبيت التطبيق
adb shell pm list packages | grep com.aidepin

# تشغيل التطبيق
adb shell am start -n com.aidepin.app/.MainActivity

# عرض السجلات
adb logcat | grep "AI Agent"
```

### 5.2 الاختبار الأساسي
1. افتح التطبيق
2. تحقق من ظهور الشاشة الرئيسية
3. اضغط على أحد الأزرار الرئيسية
4. اضغط على زر AI AGENT

---

## المرحلة 6: حل المشاكل

### مشكلة: "Gradle sync failed"
```bash
# الحل
./gradlew clean
./gradlew sync
# أو احذف مجلد .gradle وأعد المحاولة
rm -rf .gradle
```

### مشكلة: "Build failed"
```bash
# الحل
./gradlew clean build
# أو تحقق من السجلات
./gradlew build --stacktrace
```

### مشكلة: "Out of memory"
```bash
# الحل: زيادة الذاكرة المخصصة
export GRADLE_OPTS="-Xmx4g -Xms1g"
./gradlew build
```

### مشكلة: "Cannot find SDK"
```bash
# الحل: تعيين ANDROID_HOME
export ANDROID_HOME=/path/to/android/sdk
# أو في local.properties
sdk.dir=/path/to/android/sdk
```

### مشكلة: "Llama model not found"
```bash
# الحل: تحميل النموذج
python3 scripts/download_llama.py
# أو تحميل يدوي من Hugging Face
```

---

## المرحلة 7: التحسينات الاختيارية

### 7.1 تحسين الأداء
```bash
# بناء مع تحسينات
./gradlew assembleRelease --profile

# استخدام R8 بدلاً من ProGuard
# تحقق من build.gradle
```

### 7.2 تقليل حجم APK
```bash
# تفعيل minification
minifyEnabled true
shrinkResources true

# استخدام split APKs
splits {
    abi {
        enable true
        reset()
        include 'armeabi-v7a', 'arm64-v8a'
    }
}
```

### 7.3 توقيع APK
```bash
# إنشاء keystore
keytool -genkey -v -keystore my-release-key.keystore \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias my-key-alias

# توقيع APK
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 \
  -keystore my-release-key.keystore \
  app-release.apk my-key-alias

# محاذاة APK
zipalign -v 4 app-release.apk app-release-aligned.apk
```

---

## المرحلة 8: النشر على Google Play Store

### 8.1 إنشاء حساب Developer
1. اذهب إلى https://play.google.com/console
2. أنشئ حساباً جديداً
3. ادفع رسوم التسجيل ($25)

### 8.2 إنشاء تطبيق جديد
1. اضغط "Create app"
2. أدخل اسم التطبيق
3. اختر الفئة
4. ملء التفاصيل

### 8.3 رفع APK
1. اذهب إلى Release > Production
2. اضغط "Create new release"
3. اختر APK الموقعة
4. أضف الوصف والصور

### 8.4 المراجعة والنشر
1. تحقق من جميع التفاصيل
2. اضغط "Submit for review"
3. انتظر موافقة Google (عادة 24-48 ساعة)

---

## الملفات المُنتجة

بعد البناء الناجح، ستجد:

```
app/build/outputs/
├── apk/
│   ├── debug/
│   │   └── app-debug.apk (50-60 MB)
│   └── release/
│       └── app-release.apk (30-40 MB)
├── bundle/
│   └── release/
│       └── app-release.aab
└── mapping/
    └── release/
        ├── mapping.txt
        ├── seeds.txt
        └── usage.txt
```

---

## الخطوات التالية

1. ✅ بناء التطبيق
2. ✅ الاختبار على جهاز حقيقي
3. ✅ إصلاح الأخطاء
4. ✅ تحسين الأداء
5. ✅ النشر على Google Play Store

---

**آخر تحديث**: 2026-02-07
