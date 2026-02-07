import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, Pressable, FlatList, TextInput } from 'react-native';
import { ScreenContainer } from '@/components/screen-container';
import { useNodeStore, useSessionStore } from '@/lib/store';
import { cn } from '@/lib/utils';
import type { WorkerNode } from '@/lib/types';

const NodesScreen = () => {
  const { nodes, setNodes, selectedNode, setSelectedNode, isLoadingNodes } = useNodeStore();
  const { setCurrentSession } = useSessionStore();
  const [searchQuery, setSearchQuery] = useState('');
  const [filteredNodes, setFilteredNodes] = useState<WorkerNode[]>([]);

  useEffect(() => {
    // محاكاة جلب العقد
    const mockNodes: WorkerNode[] = [
      {
        id: '1',
        name: 'GPU Node 1 - US',
        location: { country: 'USA', region: 'California', latitude: 37.7749, longitude: -122.4194 },
        gpuSpecs: { model: 'RTX 4090', memory: 24, computeCapability: '8.9', count: 2 },
        pricePerHour: 0.5,
        status: 'online',
        performance: { uptime: 99.5, avgLatency: 25, rating: 4.8, totalSessions: 1250 },
        createdAt: new Date(),
        updatedAt: new Date(),
      },
      {
        id: '2',
        name: 'GPU Node 2 - EU',
        location: { country: 'Germany', region: 'Frankfurt', latitude: 50.1109, longitude: 8.6821 },
        gpuSpecs: { model: 'A100', memory: 40, computeCapability: '8.0', count: 1 },
        pricePerHour: 0.8,
        status: 'online',
        performance: { uptime: 99.8, avgLatency: 15, rating: 4.9, totalSessions: 2100 },
        createdAt: new Date(),
        updatedAt: new Date(),
      },
      {
        id: '3',
        name: 'GPU Node 3 - Asia',
        location: { country: 'Singapore', region: 'Singapore', latitude: 1.3521, longitude: 103.8198 },
        gpuSpecs: { model: 'RTX 3090', memory: 24, computeCapability: '8.6', count: 3 },
        pricePerHour: 0.4,
        status: 'busy',
        performance: { uptime: 98.9, avgLatency: 35, rating: 4.6, totalSessions: 890 },
        createdAt: new Date(),
        updatedAt: new Date(),
      },
    ];

    setNodes(mockNodes);
    setFilteredNodes(mockNodes);
  }, []);

  useEffect(() => {
    // تصفية العقد بناءً على البحث
    const filtered = nodes.filter(
      (node) =>
        node.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        node.location.country.toLowerCase().includes(searchQuery.toLowerCase())
    );
    setFilteredNodes(filtered);
  }, [searchQuery, nodes]);

  const handleConnectNode = (node: WorkerNode) => {
    setSelectedNode(node);
    // محاكاة إنشاء جلسة
    const mockSession = {
      id: `session-${Date.now()}`,
      userId: 'user-1',
      nodeId: node.id,
      startTime: new Date(),
      duration: 0,
      status: 'active' as const,
      webrtcConnection: {
        offerId: '',
        answerId: '',
        connectionState: 'connecting',
        iceServers: [],
      },
      performance: { bandwidth: 0, latency: 0, packetLoss: 0, fps: 0 },
      payment: { totalCost: 0, currency: 'SOL', status: 'pending' as const },
      serviceType: 'gaming' as const,
      serviceDetails: { gameName: 'Fortnite' },
    };
    setCurrentSession(mockSession as any);
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'online':
        return { bg: 'bg-success/20', text: 'text-success', label: 'متاح' };
      case 'busy':
        return { bg: 'bg-warning/20', text: 'text-warning', label: 'مشغول' };
      case 'offline':
        return { bg: 'bg-error/20', text: 'text-error', label: 'غير متاح' };
      default:
        return { bg: 'bg-muted/20', text: 'text-muted', label: status };
    }
  };

  return (
    <ScreenContainer className="bg-background">
      <ScrollView contentContainerStyle={{ flexGrow: 1 }} className="flex-1">
        <View className="p-6 gap-6">
          {/* شريط البحث */}
          <View className="gap-2">
            <Text className="text-lg font-bold text-foreground">العقد المتاحة</Text>
            <TextInput
              placeholder="ابحث عن عقدة..."
              placeholderTextColor="#9BA1A6"
              value={searchQuery}
              onChangeText={setSearchQuery}
              className="bg-surface rounded-xl px-4 py-3 text-foreground"
            />
          </View>

          {/* قائمة العقد */}
          <View className="gap-3">
            {filteredNodes.length > 0 ? (
              filteredNodes.map((node) => {
                const statusBadge = getStatusBadge(node.status);
                return (
                  <Pressable
                    key={node.id}
                    onPress={() => handleConnectNode(node)}
                    className={cn(
                      'bg-surface rounded-xl p-4 gap-3 active:opacity-70',
                      selectedNode?.id === node.id && 'border-2 border-primary'
                    )}
                  >
                    {/* الرأس */}
                    <View className="flex-row items-center justify-between">
                      <View className="flex-1 gap-1">
                        <Text className="text-foreground font-bold">{node.name}</Text>
                        <Text className="text-muted text-sm">
                          {node.location.country} • {node.location.region}
                        </Text>
                      </View>
                      <View className={cn('rounded-full px-3 py-1', statusBadge.bg)}>
                        <Text className={cn('text-xs font-semibold', statusBadge.text)}>
                          {statusBadge.label}
                        </Text>
                      </View>
                    </View>

                    {/* معلومات GPU */}
                    <View className="flex-row gap-4 bg-background/50 rounded-lg p-3">
                      <View className="flex-1 gap-1">
                        <Text className="text-muted text-xs">GPU</Text>
                        <Text className="text-foreground font-semibold">
                          {node.gpuSpecs.model}
                        </Text>
                      </View>
                      <View className="flex-1 gap-1">
                        <Text className="text-muted text-xs">الذاكرة</Text>
                        <Text className="text-foreground font-semibold">
                          {node.gpuSpecs.memory}GB
                        </Text>
                      </View>
                      <View className="flex-1 gap-1">
                        <Text className="text-muted text-xs">التأخير</Text>
                        <Text className="text-foreground font-semibold">
                          {node.performance.avgLatency}ms
                        </Text>
                      </View>
                    </View>

                    {/* السعر والتقييم */}
                    <View className="flex-row items-center justify-between">
                      <View className="flex-row items-center gap-2">
                        <Text className="text-2xl">⭐</Text>
                        <Text className="text-foreground font-bold">
                          {node.performance.rating}
                        </Text>
                        <Text className="text-muted text-sm">
                          ({node.performance.totalSessions})
                        </Text>
                      </View>
                      <Text className="text-lg font-bold text-primary">
                        {node.pricePerHour} SOL/ساعة
                      </Text>
                    </View>

                    {/* زر الاتصال */}
                    {node.status === 'online' && (
                      <Pressable className="bg-primary rounded-lg py-2 items-center">
                        <Text className="text-background font-semibold">الاتصال</Text>
                      </Pressable>
                    )}
                  </Pressable>
                );
              })
            ) : (
              <View className="bg-surface rounded-xl p-8 items-center">
                <Text className="text-muted text-center">لم يتم العثور على عقد</Text>
              </View>
            )}
          </View>
        </View>
      </ScrollView>
    </ScreenContainer>
  );
};

export default NodesScreen;
