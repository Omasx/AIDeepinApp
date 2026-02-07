import React, { useState } from 'react';
import { View, Text, ScrollView, Pressable, Image } from 'react-native';
import { router } from 'expo-router';
import { ScreenContainer } from '@/components/screen-container';
import { cn } from '@/lib/utils';

const OnboardingScreen = () => {
  const [currentStep, setCurrentStep] = useState(0);

  const steps = [
    {
      title: 'مرحباً بك في DePIN GPU Network',
      description: 'الوصول إلى قوة معالجة GPU لا محدودة من شبكة لامركزية',
      icon: '🚀',
    },
    {
      title: 'شبكة لامركزية',
      description: 'تتصل بعقد معالجة موزعة حول العالم توفر قوة حوسبة عالية',
      icon: '🌐',
    },
    {
      title: 'الدفع عبر Solana',
      description: 'ادفع مقابل الخدمات باستخدام عملات Solana بأمان وسرعة',
      icon: '💰',
    },
    {
      title: 'بث الألعاب والذكاء الاصطناعي',
      description: 'شغّل Fortnite واستخدم نماذج Llama 3 بدون قيود',
      icon: '🎮',
    },
  ];

  const handleNext = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      router.replace('/(tabs)/');
    }
  };

  const handleSkip = () => {
    router.replace('/(tabs)/');
  };

  const step = steps[currentStep];

  return (
    <ScreenContainer className="bg-background">
      <ScrollView contentContainerStyle={{ flexGrow: 1 }} className="flex-1">
        <View className="flex-1 justify-between py-8 px-6">
          {/* محتوى الخطوة */}
          <View className="items-center gap-8 flex-1 justify-center">
            <Text className="text-6xl">{step.icon}</Text>
            <View className="items-center gap-4">
              <Text className="text-3xl font-bold text-foreground text-center">
                {step.title}
              </Text>
              <Text className="text-lg text-muted text-center leading-relaxed">
                {step.description}
              </Text>
            </View>
          </View>

          {/* مؤشرات الخطوات */}
          <View className="flex-row justify-center gap-2 my-8">
            {steps.map((_, index) => (
              <View
                key={index}
                className={cn(
                  'h-2 rounded-full',
                  index === currentStep ? 'w-8 bg-primary' : 'w-2 bg-border'
                )}
              />
            ))}
          </View>

          {/* الأزرار */}
          <View className="gap-4">
            <Pressable
              onPress={handleNext}
              className="bg-primary rounded-full py-4 items-center"
            >
              <Text className="text-background font-semibold text-lg">
                {currentStep === steps.length - 1 ? 'ابدأ الآن' : 'التالي'}
              </Text>
            </Pressable>

            {currentStep < steps.length - 1 && (
              <Pressable
                onPress={handleSkip}
                className="py-3 items-center"
              >
                <Text className="text-muted font-semibold">تخطي</Text>
              </Pressable>
            )}
          </View>
        </View>
      </ScrollView>
    </ScreenContainer>
  );
};

export default OnboardingScreen;
