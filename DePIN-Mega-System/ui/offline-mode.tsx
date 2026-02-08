/**
 * 🌐 قائمة وضع بدون إنترنت - Offline Mode Menu
 * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 * 
 * واجهة جميلة وأنيقة لوضع بدون إنترنت مع نظام اتصال ذكي بشبكات DePIN
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  Animated,
  ActivityIndicator,
  Dimensions,
} from 'react-native';
import { Ionicons, MaterialCommunityIcons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';

interface NetworkNode {
  id: string;
  name: string;
  type: 'depin' | 'wifi' | 'cellular' | 'mesh';
  signal_strength: number;
  latency: number;
  distance: number;
  quality: 'excellent' | 'good' | 'fair' | 'poor' | 'offline';
}

interface OfflineModeProps {
  isVisible: boolean;
  onClose: () => void;
  onConnect: (network: NetworkNode) => void;
}

const { width, height } = Dimensions.get('window');

export const OfflineModeMenu: React.FC<OfflineModeProps> = ({
  isVisible,
  onClose,
  onConnect,
}) => {
  const [networks, setNetworks] = useState<NetworkNode[]>([]);
  const [selectedNetwork, setSelectedNetwork] = useState<NetworkNode | null>(null);
  const [isScanning, setIsScanning] = useState(false);
  const [isConnecting, setIsConnecting] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState<string>('');
  const [animationValue] = useState(new Animated.Value(0));

  // محاكاة مسح الشبكات
  const scanNetworks = async () => {
    setIsScanning(true);
    
    // محاكاة التأخير
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    const mockNetworks: NetworkNode[] = [
      {
        id: 'depin-1',
        name: 'DePIN Hub - الرياض',
        type: 'depin',
        signal_strength: 95,
        latency: 15,
        distance: 2.5,
        quality: 'excellent',
      },
      {
        id: 'depin-2',
        name: 'DePIN Mesh - دبي',
        type: 'mesh',
        signal_strength: 85,
        latency: 25,
        distance: 8.3,
        quality: 'good',
      },
      {
        id: 'wifi-1',
        name: 'شبكة محلية',
        type: 'wifi',
        signal_strength: 70,
        latency: 35,
        distance: 0.1,
        quality: 'fair',
      },
    ];
    
    setNetworks(mockNetworks);
    setIsScanning(false);
  };

  // الاتصال بالشبكة
  const handleConnect = async (network: NetworkNode) => {
    setIsConnecting(true);
    setSelectedNetwork(network);
    setConnectionStatus('جاري الاتصال...');
    
    // محاكاة الاتصال
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    setConnectionStatus('✅ متصل بنجاح');
    onConnect(network);
    
    setTimeout(() => {
      onClose();
    }, 1000);
  };

  // تشغيل الرسوم المتحركة
  useEffect(() => {
    if (isVisible) {
      Animated.loop(
        Animated.sequence([
          Animated.timing(animationValue, {
            toValue: 1,
            duration: 1500,
            useNativeDriver: false,
          }),
          Animated.timing(animationValue, {
            toValue: 0,
            duration: 1500,
            useNativeDriver: false,
          }),
        ])
      ).start();
    }
  }, [isVisible]);

  if (!isVisible) return null;

  const getQualityColor = (quality: string) => {
    switch (quality) {
      case 'excellent':
        return '#10B981';
      case 'good':
        return '#3B82F6';
      case 'fair':
        return '#F59E0B';
      case 'poor':
        return '#EF4444';
      default:
        return '#9CA3AF';
    }
  };

  const getQualityLabel = (quality: string) => {
    switch (quality) {
      case 'excellent':
        return 'ممتاز';
      case 'good':
        return 'جيد';
      case 'fair':
        return 'مقبول';
      case 'poor':
        return 'ضعيف';
      default:
        return 'غير متصل';
    }
  };

  const getNetworkIcon = (type: string) => {
    switch (type) {
      case 'depin':
        return 'cloud-network';
      case 'mesh':
        return 'wifi-strength-4';
      case 'wifi':
        return 'wifi';
      case 'cellular':
        return 'signal-cellular-4';
      default:
        return 'help-circle';
    }
  };

  return (
    <View style={styles.container}>
      {/* خلفية شبه شفافة */}
      <TouchableOpacity
        style={styles.backdrop}
        activeOpacity={0.8}
        onPress={onClose}
      />

      {/* القائمة الرئيسية */}
      <LinearGradient
        colors={['#1F2937', '#111827']}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
        style={styles.menu}
      >
        <ScrollView
          showsVerticalScrollIndicator={false}
          contentContainerStyle={styles.scrollContent}
        >
          {/* الرأس */}
          <View style={styles.header}>
            <View style={styles.headerTop}>
              <View style={styles.titleContainer}>
                <MaterialCommunityIcons
                  name="wifi-off"
                  size={28}
                  color="#EF4444"
                  style={styles.headerIcon}
                />
                <Text style={styles.title}>وضع بدون إنترنت</Text>
              </View>
              <TouchableOpacity onPress={onClose}>
                <Ionicons name="close" size={24} color="#9CA3AF" />
              </TouchableOpacity>
            </View>
            <Text style={styles.subtitle}>
              اتصل بشبكات DePIN اللامركزية للاستمرار في العمل
            </Text>
          </View>

          {/* زر المسح */}
          <TouchableOpacity
            style={[styles.scanButton, isScanning && styles.scanButtonActive]}
            onPress={scanNetworks}
            disabled={isScanning}
          >
            <LinearGradient
              colors={isScanning ? ['#3B82F6', '#1E40AF'] : ['#10B981', '#047857']}
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 1 }}
              style={styles.scanButtonGradient}
            >
              {isScanning ? (
                <>
                  <ActivityIndicator color="#FFF" size="small" />
                  <Text style={styles.scanButtonText}>جاري المسح...</Text>
                </>
              ) : (
                <>
                  <MaterialCommunityIcons
                    name="wifi-find"
                    size={20}
                    color="#FFF"
                  />
                  <Text style={styles.scanButtonText}>مسح الشبكات</Text>
                </>
              )}
            </LinearGradient>
          </TouchableOpacity>

          {/* قائمة الشبكات */}
          {networks.length > 0 ? (
            <View style={styles.networksContainer}>
              <Text style={styles.networksTitle}>
                الشبكات المتاحة ({networks.length})
              </Text>

              {networks.map((network, index) => (
                <TouchableOpacity
                  key={network.id}
                  style={[
                    styles.networkCard,
                    selectedNetwork?.id === network.id && styles.networkCardSelected,
                  ]}
                  onPress={() => handleConnect(network)}
                  disabled={isConnecting}
                  activeOpacity={0.7}
                >
                  <LinearGradient
                    colors={
                      selectedNetwork?.id === network.id
                        ? ['#3B82F6', '#1E40AF']
                        : ['#374151', '#1F2937']
                    }
                    start={{ x: 0, y: 0 }}
                    end={{ x: 1, y: 1 }}
                    style={styles.networkCardGradient}
                  >
                    {/* أيقونة الشبكة */}
                    <View style={styles.networkIcon}>
                      <MaterialCommunityIcons
                        name={getNetworkIcon(network.type)}
                        size={24}
                        color={getQualityColor(network.quality)}
                      />
                    </View>

                    {/* معلومات الشبكة */}
                    <View style={styles.networkInfo}>
                      <Text style={styles.networkName}>{network.name}</Text>
                      <View style={styles.networkDetails}>
                        <View style={styles.detailItem}>
                          <MaterialCommunityIcons
                            name="signal-cellular-3"
                            size={14}
                            color="#9CA3AF"
                          />
                          <Text style={styles.detailText}>
                            {network.signal_strength}%
                          </Text>
                        </View>
                        <View style={styles.detailItem}>
                          <MaterialCommunityIcons
                            name="speedometer"
                            size={14}
                            color="#9CA3AF"
                          />
                          <Text style={styles.detailText}>
                            {network.latency}ms
                          </Text>
                        </View>
                        <View style={styles.detailItem}>
                          <MaterialCommunityIcons
                            name="map-marker-distance"
                            size={14}
                            color="#9CA3AF"
                          />
                          <Text style={styles.detailText}>
                            {network.distance} km
                          </Text>
                        </View>
                      </View>
                    </View>

                    {/* شارة الجودة */}
                    <View
                      style={[
                        styles.qualityBadge,
                        { backgroundColor: getQualityColor(network.quality) },
                      ]}
                    >
                      <Text style={styles.qualityText}>
                        {getQualityLabel(network.quality)}
                      </Text>
                    </View>

                    {/* أيقونة الاتصال */}
                    {selectedNetwork?.id === network.id && (
                      <View style={styles.connectingIndicator}>
                        {isConnecting ? (
                          <ActivityIndicator color="#FFF" size="small" />
                        ) : (
                          <Ionicons name="checkmark-circle" size={24} color="#10B981" />
                        )}
                      </View>
                    )}
                  </LinearGradient>
                </TouchableOpacity>
              ))}
            </View>
          ) : (
            <View style={styles.emptyState}>
              <MaterialCommunityIcons
                name="wifi-off"
                size={48}
                color="#6B7280"
              />
              <Text style={styles.emptyStateText}>
                لم يتم العثور على شبكات متاحة
              </Text>
              <Text style={styles.emptyStateSubtext}>
                اضغط على "مسح الشبكات" للبحث عن شبكات DePIN
              </Text>
            </View>
          )}

          {/* حالة الاتصال */}
          {connectionStatus && (
            <View style={styles.statusContainer}>
              <Text style={styles.statusText}>{connectionStatus}</Text>
            </View>
          )}

          {/* معلومات مساعدة */}
          <View style={styles.infoBox}>
            <MaterialCommunityIcons
              name="information-outline"
              size={20}
              color="#3B82F6"
            />
            <Text style={styles.infoText}>
              شبكات DePIN توفر اتصالاً لامركزياً موثوقاً عند انقطاع الإنترنت العادي
            </Text>
          </View>
        </ScrollView>
      </LinearGradient>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    ...StyleSheet.absoluteFillObject,
    justifyContent: 'flex-end',
    zIndex: 1000,
  },
  backdrop: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
  },
  menu: {
    width: '100%',
    maxHeight: height * 0.85,
    borderTopLeftRadius: 24,
    borderTopRightRadius: 24,
    paddingTop: 20,
  },
  scrollContent: {
    paddingHorizontal: 16,
    paddingBottom: 32,
  },
  header: {
    marginBottom: 24,
  },
  headerTop: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  titleContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  headerIcon: {
    marginRight: 12,
  },
  title: {
    fontSize: 22,
    fontWeight: '700',
    color: '#FFF',
  },
  subtitle: {
    fontSize: 14,
    color: '#D1D5DB',
    marginTop: 8,
  },
  scanButton: {
    marginBottom: 24,
    borderRadius: 12,
    overflow: 'hidden',
  },
  scanButtonActive: {
    opacity: 0.8,
  },
  scanButtonGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 14,
    paddingHorizontal: 16,
  },
  scanButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#FFF',
    marginLeft: 8,
  },
  networksContainer: {
    marginBottom: 24,
  },
  networksTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#E5E7EB',
    marginBottom: 12,
  },
  networkCard: {
    marginBottom: 12,
    borderRadius: 12,
    overflow: 'hidden',
  },
  networkCardSelected: {
    borderWidth: 2,
    borderColor: '#3B82F6',
  },
  networkCardGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 14,
    paddingHorizontal: 14,
  },
  networkIcon: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  networkInfo: {
    flex: 1,
  },
  networkName: {
    fontSize: 15,
    fontWeight: '600',
    color: '#FFF',
    marginBottom: 6,
  },
  networkDetails: {
    flexDirection: 'row',
    gap: 12,
  },
  detailItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  detailText: {
    fontSize: 12,
    color: '#9CA3AF',
  },
  qualityBadge: {
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 6,
    marginRight: 8,
  },
  qualityText: {
    fontSize: 11,
    fontWeight: '600',
    color: '#FFF',
  },
  connectingIndicator: {
    marginLeft: 8,
  },
  emptyState: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 40,
  },
  emptyStateText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#E5E7EB',
    marginTop: 12,
  },
  emptyStateSubtext: {
    fontSize: 13,
    color: '#9CA3AF',
    marginTop: 6,
    textAlign: 'center',
  },
  statusContainer: {
    backgroundColor: 'rgba(16, 185, 129, 0.1)',
    borderRadius: 8,
    paddingVertical: 12,
    paddingHorizontal: 14,
    marginBottom: 16,
    borderLeftWidth: 4,
    borderLeftColor: '#10B981',
  },
  statusText: {
    fontSize: 14,
    color: '#10B981',
    fontWeight: '600',
  },
  infoBox: {
    flexDirection: 'row',
    backgroundColor: 'rgba(59, 130, 246, 0.1)',
    borderRadius: 8,
    paddingVertical: 12,
    paddingHorizontal: 14,
    borderLeftWidth: 4,
    borderLeftColor: '#3B82F6',
  },
  infoText: {
    fontSize: 13,
    color: '#93C5FD',
    marginLeft: 10,
    flex: 1,
  },
});
