import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, Pressable, FlatList } from 'react-native';
import { ScreenContainer } from '@/components/screen-container';
import { useUserStore } from '@/lib/store';
import { cn } from '@/lib/utils';

const WalletScreen = () => {
  const { wallet, user } = useUserStore();
  const [transactions, setTransactions] = useState<any[]>([]);

  useEffect(() => {
    // محاكاة جلب المعاملات
    setTransactions([
      {
        id: '1',
        type: 'payment',
        amount: 0.5,
        description: 'دفع لجلسة GPU',
        timestamp: new Date(),
        status: 'completed',
      },
      {
        id: '2',
        type: 'deposit',
        amount: 5.0,
        description: 'إيداع من المحفظة',
        timestamp: new Date(Date.now() - 86400000),
        status: 'completed',
      },
    ]);
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'text-success';
      case 'pending':
        return 'text-warning';
      case 'failed':
        return 'text-error';
      default:
        return 'text-muted';
    }
  };

  const getTypeLabel = (type: string) => {
    switch (type) {
      case 'payment':
        return 'دفع';
      case 'deposit':
        return 'إيداع';
      case 'withdrawal':
        return 'سحب';
      case 'refund':
        return 'استرجاع';
      default:
        return type;
    }
  };

  return (
    <ScreenContainer className="bg-background">
      <ScrollView contentContainerStyle={{ flexGrow: 1 }} className="flex-1">
        <View className="p-6 gap-6">
          {/* بطاقة الرصيد */}
          <View className="bg-gradient-to-r from-primary to-primary/80 rounded-2xl p-6 gap-4">
            <Text className="text-white/80 text-sm">الرصيد الحالي</Text>
            <Text className="text-4xl font-bold text-white">
              {wallet?.balance || 0} SOL
            </Text>
            <Text className="text-white/60 text-xs font-mono">
              {wallet?.address
                ? wallet.address.slice(0, 10) + '...' + wallet.address.slice(-10)
                : 'غير متصل'}
            </Text>
          </View>

          {/* الأزرار السريعة */}
          <View className="flex-row gap-3">
            <Pressable className="flex-1 bg-surface rounded-xl p-4 items-center active:opacity-70">
              <Text className="text-2xl mb-2">📤</Text>
              <Text className="text-foreground font-semibold text-sm">استقبال</Text>
            </Pressable>
            <Pressable className="flex-1 bg-surface rounded-xl p-4 items-center active:opacity-70">
              <Text className="text-2xl mb-2">📥</Text>
              <Text className="text-foreground font-semibold text-sm">إرسال</Text>
            </Pressable>
            <Pressable className="flex-1 bg-surface rounded-xl p-4 items-center active:opacity-70">
              <Text className="text-2xl mb-2">📋</Text>
              <Text className="text-foreground font-semibold text-sm">نسخ</Text>
            </Pressable>
          </View>

          {/* سجل المعاملات */}
          <View className="gap-3">
            <Text className="text-lg font-bold text-foreground">المعاملات الأخيرة</Text>
            {transactions.length > 0 ? (
              <View className="gap-2">
                {transactions.map((tx) => (
                  <View
                    key={tx.id}
                    className="bg-surface rounded-xl p-4 flex-row items-center justify-between"
                  >
                    <View className="flex-1 gap-1">
                      <Text className="text-foreground font-semibold">
                        {getTypeLabel(tx.type)}
                      </Text>
                      <Text className="text-muted text-sm">{tx.description}</Text>
                      <Text className="text-muted text-xs">
                        {tx.timestamp.toLocaleDateString('ar-SA')}
                      </Text>
                    </View>
                    <View className="items-end gap-1">
                      <Text
                        className={cn(
                          'font-bold text-lg',
                          tx.type === 'deposit' || tx.type === 'refund'
                            ? 'text-success'
                            : 'text-foreground'
                        )}
                      >
                        {tx.type === 'deposit' || tx.type === 'refund' ? '+' : '-'}
                        {tx.amount} SOL
                      </Text>
                      <Text className={cn('text-xs font-semibold', getStatusColor(tx.status))}>
                        {tx.status === 'completed'
                          ? 'مكتملة'
                          : tx.status === 'pending'
                          ? 'قيد الانتظار'
                          : 'فشلت'}
                      </Text>
                    </View>
                  </View>
                ))}
              </View>
            ) : (
              <View className="bg-surface rounded-xl p-8 items-center">
                <Text className="text-muted text-center">لا توجد معاملات بعد</Text>
              </View>
            )}
          </View>
        </View>
      </ScrollView>
    </ScreenContainer>
  );
};

export default WalletScreen;
