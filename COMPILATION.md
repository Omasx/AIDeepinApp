# 🔨 تعليمات البناء والتجميع

## المتطلبات

- Android Studio 2023.1 أو أحدث
- JDK 11 أو أحدث
- Gradle 8.0 أو أحدث
- Android SDK 34

## خطوات البناء

### 1. فتح المشروع في Android Studio

```bash
cd /home/ubuntu/AIDeepinApp-Final
```

### 2. مزامنة Gradle

```bash
./gradlew sync
```

### 3. بناء التطبيق (Debug)

```bash
./gradlew assembleDebug
```

سيتم إنشاء ملف APK في:
```
app/build/outputs/apk/debug/app-debug.apk
```

### 4. بناء التطبيق (Release)

```bash
./gradlew assembleRelease
```

سيتم إنشاء ملف APK في:
```
app/build/outputs/apk/release/app-release.apk
```

## التثبيت على الهاتف

### الطريقة 1: عبر ADB

```bash
# Debug
adb install app/build/outputs/apk/debug/app-debug.apk

# Release
adb install app/build/outputs/apk/release/app-release.apk
```

### الطريقة 2: عبر Android Studio

1. اختر Run > Run 'app'
2. اختر جهازك من القائمة
3. اضغط OK

## حل المشاكل الشائعة

### مشكلة: "Gradle sync failed"

**الحل:**
```bash
./gradlew clean
./gradlew sync
```

### مشكلة: "Build failed"

**الحل:**
```bash
./gradlew clean build
```

### مشكلة: "Cannot find SDK"

**الحل:**
تأكد من تثبيت Android SDK 34 وتعيين ANDROID_HOME بشكل صحيح.

## الخيارات المتقدمة

### بناء مع Proguard

```bash
./gradlew assembleRelease -Pproguard=true
```

### بناء مع تحسينات الأداء

```bash
./gradlew assembleRelease --profile
```

### بناء متعدد الأنظمة

```bash
./gradlew assembleRelease -Pmulti-arch=true
```

## التحقق من البناء

```bash
# التحقق من ملف APK
aapt dump badging app/build/outputs/apk/release/app-release.apk

# قائمة الأذونات
aapt dump permissions app/build/outputs/apk/release/app-release.apk
```

## الأحجام

- **Debug APK**: ~50-60 MB
- **Release APK**: ~30-40 MB (بعد التحسينات)

## الإصدار

لنشر التطبيق على Google Play Store:

1. توقيع APK:
```bash
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 \
  -keystore my-release-key.keystore \
  app/build/outputs/apk/release/app-release.apk \
  alias_name
```

2. محاذاة APK:
```bash
zipalign -v 4 app-release.apk app-release-aligned.apk
```

---

**آخر تحديث**: 2026-02-07
