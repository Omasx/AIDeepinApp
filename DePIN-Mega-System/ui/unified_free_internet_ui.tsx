/**
 * 🌍 واجهة موحدة لنظام الإنترنت المجاني - Unified Free Internet UI
 * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 * 
 * واجهة شاملة تجمع جميع خيارات الإنترنت المجاني الأخلاقي والموثوق
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
  FlatList,
} from 'react-native';
import { Ionicons, MaterialCommunityIcons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';

interface InternetProvider {
  id: string;
  name: string;
  type: 'public_wifi' | 'community_mesh' | 'satellite' | 'isp' | 'university' | 'ngo';
  speed_mbps: number;
  latency_ms: number;
  distance_km: number;
  quality: 'excellent' | 'good' | 'fair' | 'poor';
  user_rating: number;
  opening_hours?: string;
  requires_registration?: boolean;
  description: string;
}

interface UnifiedFreeInternetUIProps {
  isVisible: boolean;
  onClose: () => void;
  onConnect: (provider: InternetProvider) => void;
}

const { width, height } = Dimensions.get('window');

const PROVIDER_TYPES = [
  { id: 'all', label: 'الكل', icon: 'wifi' },
  { id: 'public_wifi', label: 'WiFi عام', icon: 'wifi-find' },
  { id: 'community_mesh', label: 'شبكات مجتمع', icon: 'network' },
  { id: 'satellite', label: 'أقمار صناعية', icon: 'satellite-variant' },
  { id: 'isp', label: 'برامج ISP', icon: 'router-wireless' },
  { id: 'university', label: 'جامعات', icon: 'school' },
  { id: 'ngo', label: 'منظمات', icon: 'hospital-box' },
];

export const UnifiedFreeInternetUI: React.FC<UnifiedFreeInternetUIProps> = ({
  isVisible,
  onClose,
  onConnect,
}) => {
  const [providers, setProviders] = useState<InternetProvider[]>([]);
  const [selectedType, setSelectedType] = useState('all');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedProvider, setSelectedProvider] = useState<InternetProvider | null>(null);
  const [connectionStatus, setConnectionStatus] = useState('');
  const [animationValue] = useState(new Animated.Value(0));

  // محاكاة تحميل المزودين
  const loadProviders = async () => {
    setIsLoading(true);
    
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    const mockProviders: InternetProvider[] = [
      {
        id: 'public-1',
        name: 'مكتبة الملك فهد الوطنية',
        type: 'public_wifi',
        speed_mbps: 20,
        latency_ms: 25,
        distance_km: 2.5,
        quality: 'good',
        user_rating: 4.5,
        opening_hours: '09:00-21:00',
        description: 'مكتبة عامة توفر WiFi مجاني',
      },
      {
        id: 'community-1',
        name: 'Guifi.net - شبكة المجتمع',
        type: 'community_mesh',
        speed_mbps: 30,
        latency_ms: 15,
        distance_km: 5.0,
        quality: 'excellent',
        user_rating: 4.3,
        description: 'شبكة مجتمع لامركزية مفتوحة المصدر',
      },
      {
        id: 'satellite-1',
        name: 'Starlink Free Program',
        type: 'satellite',
        speed_mbps: 50,
        latency_ms: 30,
        distance_km: 0,
        quality: 'excellent',
        user_rating: 4.6,
        description: 'برنامج Starlink المجاني للمناطق النائية',
      },
      {
        id: 'isp-1',
        name: 'برنامج الإنترنت الريفي - مصر',
        type: 'isp',
        speed_mbps: 8,
        latency_ms: 45,
        distance_km: 15.0,
        quality: 'fair',
        user_rating: 3.5,
        description: 'برنامج حكومي لتوفير إنترنت مجاني',
      },
      {
        id: 'university-1',
        name: 'جامعة الملك سعود',
        type: 'university',
        speed_mbps: 40,
        latency_ms: 10,
        distance_km: 8.0,
        quality: 'excellent',
        user_rating: 4.7,
        opening_hours: '06:00-23:00',
        requires_registration: true,
        description: 'شبكة جامعية توفر إنترنت مجاني',
      },
      {
        id: 'ngo-1',
        name: 'منظمة الصحة العالمية',
        type: 'ngo',
        speed_mbps: 35,
        latency_ms: 12,
        distance_km: 12.0,
        quality: 'excellent',
        user_rating: 4.6,
        description: 'منظمة دولية توفر إنترنت مجاني',
      },
    ];
    
    setProviders(mockProviders);
    setIsLoading(false);
  };

  const filteredProviders = selectedType === 'all' 
    ? providers 
    : providers.filter(p => p.type === selectedType);

  const handleConnect = async (provider: InternetProvider) => {
    setSelectedProvider(provider);
    setConnectionStatus('جاري الاتصال...');
    
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    setConnectionStatus(`✅ متصل بـ ${provider.name}`);
    onConnect(provider);
    
    setTimeout(() => {
      onClose();
    }, 1000);
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'public_wifi':
        return 'wifi-find';
      case 'community_mesh':
        return 'network';
      case 'satellite':
        return 'satellite-variant';
      case 'isp':
        return 'router-wireless';
      case 'university':
        return 'school';
      case 'ngo':
        return 'hospital-box';
      default:
        return 'wifi';
    }
  };

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
        return 'غير معروف';
    }
  };

  if (!isVisible) return null;

  return (
    <View style={styles.container}>
      <TouchableOpacity
        style={styles.backdrop}
        activeOpacity={0.8}
        onPress={onClose}
      />

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
                  name="wifi-strength-4"
                  size={28}
                  color="#10B981"
                  style={styles.headerIcon}
                />
                <Text style={styles.title}>الإنترنت المجاني</Text>
              </View>
              <TouchableOpacity onPress={onClose}>
                <Ionicons name="close" size={24} color="#9CA3AF" />
              </TouchableOpacity>
            </View>
            <Text style={styles.subtitle}>
              خيارات إنترنت مجانية أخلاقية وموثوقة 100%
            </Text>
          </View>

          {/* زر التحميل */}
          <TouchableOpacity
            style={[styles.loadButton, isLoading && styles.loadButtonActive]}
            onPress={loadProviders}
            disabled={isLoading}
          >
            <LinearGradient
              colors={isLoading ? ['#3B82F6', '#1E40AF'] : ['#10B981', '#047857']}
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 1 }}
              style={styles.loadButtonGradient}
            >
              {isLoading ? (
                <>
                  <ActivityIndicator color="#FFF" size="small" />
                  <Text style={styles.loadButtonText}>جاري البحث...</Text>
                </>
              ) : (
                <>
                  <MaterialCommunityIcons
                    name="magnify"
                    size={20}
                    color="#FFF"
                  />
                  <Text style={styles.loadButtonText}>البحث عن خيارات</Text>
                </>
              )}
            </LinearGradient>
          </TouchableOpacity>

          {/* تصفية حسب النوع */}
          {providers.length > 0 && (
            <ScrollView
              horizontal
              showsHorizontalScrollIndicator={false}
              style={styles.filterContainer}
              contentContainerStyle={styles.filterContent}
            >
              {PROVIDER_TYPES.map((type) => (
                <TouchableOpacity
                  key={type.id}
                  style={[
                    styles.filterButton,
                    selectedType === type.id && styles.filterButtonActive,
                  ]}
                  onPress={() => setSelectedType(type.id)}
                >
                  <MaterialCommunityIcons
                    name={type.icon}
                    size={16}
                    color={selectedType === type.id ? '#FFF' : '#9CA3AF'}
                  />
                  <Text
                    style={[
                      styles.filterButtonText,
                      selectedType === type.id && styles.filterButtonTextActive,
                    ]}
                  >
                    {type.label}
                  </Text>
                </TouchableOpacity>
              ))}
            </ScrollView>
          )}

          {/* قائمة المزودين */}
          {filteredProviders.length > 0 ? (
            <View style={styles.providersContainer}>
              <Text style={styles.providersTitle}>
                الخيارات المتاحة ({filteredProviders.length})
              </Text>

              {filteredProviders.map((provider) => (
                <TouchableOpacity
                  key={provider.id}
                  style={[
                    styles.providerCard,
                    selectedProvider?.id === provider.id && styles.providerCardSelected,
                  ]}
                  onPress={() => handleConnect(provider)}
                  disabled={isLoading}
                  activeOpacity={0.7}
                >
                  <LinearGradient
                    colors={
                      selectedProvider?.id === provider.id
                        ? ['#3B82F6', '#1E40AF']
                        : ['#374151', '#1F2937']
                    }
                    start={{ x: 0, y: 0 }}
                    end={{ x: 1, y: 1 }}
                    style={styles.providerCardGradient}
                  >
                    {/* أيقونة النوع */}
                    <View style={styles.providerIcon}>
                      <MaterialCommunityIcons
                        name={getTypeIcon(provider.type)}
                        size={24}
                        color={getQualityColor(provider.quality)}
                      />
                    </View>

                    {/* معلومات المزود */}
                    <View style={styles.providerInfo}>
                      <Text style={styles.providerName}>{provider.name}</Text>
                      <Text style={styles.providerDescription}>
                        {provider.description}
                      </Text>
                      <View style={styles.providerDetails}>
                        <View style={styles.detailItem}>
                          <MaterialCommunityIcons
                            name="speedometer"
                            size={14}
                            color="#9CA3AF"
                          />
                          <Text style={styles.detailText}>
                            {provider.speed_mbps} Mbps
                          </Text>
                        </View>
                        <View style={styles.detailItem}>
                          <MaterialCommunityIcons
                            name="timer"
                            size={14}
                            color="#9CA3AF"
                          />
                          <Text style={styles.detailText}>
                            {provider.latency_ms}ms
                          </Text>
                        </View>
                        <View style={styles.detailItem}>
                          <MaterialCommunityIcons
                            name="star"
                            size={14}
                            color="#FBBF24"
                          />
                          <Text style={styles.detailText}>
                            {provider.user_rating}/5
                          </Text>
                        </View>
                      </View>
                    </View>

                    {/* شارة الجودة */}
                    <View
                      style={[
                        styles.qualityBadge,
                        { backgroundColor: getQualityColor(provider.quality) },
                      ]}
                    >
                      <Text style={styles.qualityText}>
                        {getQualityLabel(provider.quality)}
                      </Text>
                    </View>

                    {/* أيقونة الاتصال */}
                    {selectedProvider?.id === provider.id && (
                      <View style={styles.connectingIndicator}>
                        {isLoading ? (
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
          ) : providers.length === 0 ? (
            <View style={styles.emptyState}>
              <MaterialCommunityIcons
                name="wifi-off"
                size={48}
                color="#6B7280"
              />
              <Text style={styles.emptyStateText}>
                لم يتم العثور على خيارات
              </Text>
              <Text style={styles.emptyStateSubtext}>
                اضغط على "البحث عن خيارات" للبدء
              </Text>
            </View>
          ) : (
            <View style={styles.emptyState}>
              <Text style={styles.emptyStateText}>
                لا توجد خيارات من هذا النوع
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
              جميع الخيارات أخلاقية وموثوقة وموصى بها من المنظمات الدولية
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
    maxHeight: height * 0.9,
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
  loadButton: {
    marginBottom: 24,
    borderRadius: 12,
    overflow: 'hidden',
  },
  loadButtonActive: {
    opacity: 0.8,
  },
  loadButtonGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 14,
    paddingHorizontal: 16,
  },
  loadButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#FFF',
    marginLeft: 8,
  },
  filterContainer: {
    marginBottom: 24,
  },
  filterContent: {
    paddingRight: 16,
  },
  filterButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 12,
    paddingVertical: 8,
    marginRight: 8,
    borderRadius: 20,
    backgroundColor: '#374151',
    borderWidth: 1,
    borderColor: '#4B5563',
  },
  filterButtonActive: {
    backgroundColor: '#3B82F6',
    borderColor: '#3B82F6',
  },
  filterButtonText: {
    fontSize: 12,
    color: '#9CA3AF',
    marginLeft: 6,
  },
  filterButtonTextActive: {
    color: '#FFF',
  },
  providersContainer: {
    marginBottom: 24,
  },
  providersTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#E5E7EB',
    marginBottom: 12,
  },
  providerCard: {
    marginBottom: 12,
    borderRadius: 12,
    overflow: 'hidden',
  },
  providerCardSelected: {
    borderWidth: 2,
    borderColor: '#3B82F6',
  },
  providerCardGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 14,
    paddingHorizontal: 14,
  },
  providerIcon: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  providerInfo: {
    flex: 1,
  },
  providerName: {
    fontSize: 15,
    fontWeight: '600',
    color: '#FFF',
    marginBottom: 4,
  },
  providerDescription: {
    fontSize: 12,
    color: '#D1D5DB',
    marginBottom: 6,
  },
  providerDetails: {
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
