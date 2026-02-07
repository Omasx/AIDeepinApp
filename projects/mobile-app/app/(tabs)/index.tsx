import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, Pressable } from 'react-native';
import { ScreenContainer } from '@/components/screen-container';
import { useUserStore, useSessionStore, useConnectionStore } from '@/lib/store';
import { router } from 'expo-router';

export default function HomeScreen() {
  const { user, wallet } = useUserStore();
  const { currentSession } = useSessionStore();
  const { connectionState } = useConnectionStore();
  const [isOnboarded, setIsOnboarded] = useState(false);

  useEffect(() => {
    if (!user || !wallet) {
      router.replace('/onboarding');
    } else {
      setIsOnboarded(true);
    }
  }, [user, wallet]);

  if (!isOnboarded) {
    return (
      <ScreenContainer className="bg-background items-center justify-center">
        <Text className="text-lg text-muted">جاري التحميل...</Text>
      </ScreenContainer>
    );
  }

  return (
    <ScreenContainer className="bg-background">
      <ScrollView contentContainerStyle={{ flexGrow: 1 }} className="flex-1">
        <View className="p-6 gap-6">
          {/* رسالة الترحيب */}
          <View className="gap-2">
            <Text className="text-3xl font-bold text-foreground">
              مرحباً، {user?.username || 'المستخدم'}!
            </Text>
            <Text className="text-muted">الوصول إلى قوة معالجة GPU لا محدودة</Text>
          </View>

          {/* بطاقة الرصيد السريعة */}
          <View className="bg-gradient-to-r from-primary to-primary/80 rounded-2xl p-6 gap-2">
            <Text className="text-white/80 text-sm">الرصيد الحالي</Text>
            <Text className="text-3xl font-bold text-white">{wallet?.balance || 0} SOL</Text>
          </View>

          {/* حالة الاتصال */}
          <View className="bg-surface rounded-xl p-4 gap-3">
            <View className="flex-row items-center justify-between">
              <Text className="text-foreground font-semibold">حالة الاتصال</Text>
              <View
                className={connectionState.isConnected ? 'w-3 h-3 rounded-full bg-success' : 'w-3 h-3 rounded-full bg-error'}
              />
            </View>
            {currentSession ? (
              <View className="gap-2">
                <Text className="text-muted text-sm">جلسة نشطة</Text>
                <Text className="text-foreground font-semibold">
                  {currentSession.serviceDetails.gameName || 'خدمة الحوسبة'}
                </Text>
                <Text className="text-muted text-xs">
                  التكلفة: {currentSession.payment.totalCost} SOL
                </Text>
              </View>
            ) : (
              <Text className="text-muted text-sm">لا توجد جلسة نشطة</Text>
            )}
          </View>

          {/* الخيارات السريعة */}
          <View className="gap-3">
            <Text className="text-lg font-bold text-foreground">الخيارات السريعة</Text>
            <View className="gap-2">
              <Pressable className="bg-surface rounded-xl p-4 flex-row items-center justify-between active:opacity-70">
                <View className="flex-row items-center gap-3">
                  <Text className="text-2xl">🎮</Text>
                  <View>
                    <Text className="text-foreground font-semibold">تشغيل لعبة</Text>
                    <Text className="text-muted text-xs">Fortnite وغيرها</Text>
                  </View>
                </View>
                <Text className="text-muted">›</Text>
              </Pressable>

              <Pressable className="bg-surface rounded-xl p-4 flex-row items-center justify-between active:opacity-70">
                <View className="flex-row items-center gap-3">
                  <Text className="text-2xl">🤖</Text>
                  <View>
                    <Text className="text-foreground font-semibold">استخدام AI</Text>
                    <Text className="text-muted text-xs">Llama 3 والنماذج الأخرى</Text>
                  </View>
                </View>
                <Text className="text-muted">›</Text>
              </Pressable>

              <Pressable className="bg-surface rounded-xl p-4 flex-row items-center justify-between active:opacity-70">
                <View className="flex-row items-center gap-3">
                  <Text className="text-2xl">💻</Text>
                  <View>
                    <Text className="text-foreground font-semibold">اختيار عقدة</Text>
                    <Text className="text-muted text-xs">الاتصال بعقد المعالجة</Text>
                  </View>
                </View>
                <Text className="text-muted">›</Text>
              </Pressable>
            </View>
          </View>

          {/* معلومات الشبكة */}
          <View className="bg-surface rounded-xl p-4 gap-3">
            <Text className="text-foreground font-semibold">معلومات الشبكة</Text>
            <View className="flex-row justify-between">
              <View>
                <Text className="text-muted text-xs">العقد المتاحة</Text>
                <Text className="text-foreground font-bold text-lg">24</Text>
              </View>
              <View>
                <Text className="text-muted text-xs">متوسط التأخير</Text>
                <Text className="text-foreground font-bold text-lg">25ms</Text>
              </View>
              <View>
                <Text className="text-muted text-xs">التوفر</Text>
                <Text className="text-success font-bold text-lg">99.8%</Text>
              </View>
            </View>
          </View>
        </View>
      </ScrollView>
    </ScreenContainer>
  );
}
