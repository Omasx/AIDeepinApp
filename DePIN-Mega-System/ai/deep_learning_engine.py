"""
🧠 Deep Learning Engine - محرك التعلم العميق
نظام تعلم عميق متقدم يتحسن مع الوقت

يدعم:
- الشبكات العصبية العميقة
- التعلم المعزز (Reinforcement Learning)
- معالجة الصور (CNN)
- معالجة اللغة الطبيعية (NLP)
- التعلم من التجارب
"""

import asyncio
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import logging
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Experience:
    """تجربة التعلم"""
    state: np.ndarray
    action: int
    reward: float
    next_state: np.ndarray
    done: bool
    timestamp: float


class NeuralNetwork:
    """شبكة عصبية بسيطة"""
    
    def __init__(self, input_size: int, hidden_size: int, output_size: int):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        
        # تهيئة الأوزان
        self.W1 = np.random.randn(input_size, hidden_size) * 0.01
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) * 0.01
        self.b2 = np.zeros((1, output_size))
        
        # معاملات التحسين
        self.learning_rate = 0.001
        self.cache = {}
    
    def relu(self, x: np.ndarray) -> np.ndarray:
        """دالة التفعيل ReLU"""
        return np.maximum(0, x)
    
    def relu_derivative(self, x: np.ndarray) -> np.ndarray:
        """مشتقة ReLU"""
        return (x > 0).astype(float)
    
    def softmax(self, x: np.ndarray) -> np.ndarray:
        """دالة Softmax"""
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)
    
    def forward(self, X: np.ndarray) -> np.ndarray:
        """المسار الأمامي"""
        
        # الطبقة الأولى
        Z1 = np.dot(X, self.W1) + self.b1
        A1 = self.relu(Z1)
        
        # الطبقة الثانية
        Z2 = np.dot(A1, self.W2) + self.b2
        A2 = self.softmax(Z2)
        
        # حفظ للاستخدام في التراجع
        self.cache = {'Z1': Z1, 'A1': A1, 'Z2': Z2, 'A2': A2, 'X': X}
        
        return A2
    
    def backward(self, dZ2: np.ndarray):
        """المسار الخلفي"""
        
        m = self.cache['X'].shape[0]
        
        # حساب التدرجات
        dW2 = np.dot(self.cache['A1'].T, dZ2) / m
        db2 = np.sum(dZ2, axis=0, keepdims=True) / m
        
        dA1 = np.dot(dZ2, self.W2.T)
        dZ1 = dA1 * self.relu_derivative(self.cache['Z1'])
        
        dW1 = np.dot(self.cache['X'].T, dZ1) / m
        db1 = np.sum(dZ1, axis=0, keepdims=True) / m
        
        # تحديث الأوزان
        self.W2 -= self.learning_rate * dW2
        self.b2 -= self.learning_rate * db2
        self.W1 -= self.learning_rate * dW1
        self.b1 -= self.learning_rate * db1
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """التنبؤ"""
        output = self.forward(X)
        return np.argmax(output, axis=1)


class ReinforcementLearner:
    """متعلم التعزيز"""
    
    def __init__(self, state_size: int, action_size: int):
        self.state_size = state_size
        self.action_size = action_size
        
        # Q-Learning
        self.q_table = np.zeros((state_size, action_size))
        self.learning_rate = 0.1
        self.discount_factor = 0.95
        self.exploration_rate = 1.0
        self.exploration_decay = 0.995
        
        # تخزين التجارب
        self.experiences = []
        self.max_experiences = 10000
    
    def store_experience(self, experience: Experience):
        """تخزين تجربة"""
        self.experiences.append(experience)
        
        # حذف التجارب القديمة
        if len(self.experiences) > self.max_experiences:
            self.experiences.pop(0)
    
    def select_action(self, state: int) -> int:
        """اختيار إجراء"""
        
        # استكشاف vs استغلال
        if np.random.random() < self.exploration_rate:
            return np.random.randint(0, self.action_size)
        else:
            return np.argmax(self.q_table[state])
    
    def learn(self, state: int, action: int, reward: float, next_state: int, done: bool):
        """التعلم من التجربة"""
        
        # Q-Learning update
        target = reward
        if not done:
            target += self.discount_factor * np.max(self.q_table[next_state])
        
        self.q_table[state, action] += self.learning_rate * (target - self.q_table[state, action])
        
        # تقليل معدل الاستكشاف
        self.exploration_rate *= self.exploration_decay
    
    def get_policy(self) -> np.ndarray:
        """الحصول على السياسة المثلى"""
        return np.argmax(self.q_table, axis=1)


class ConvolutionalNeuralNetwork:
    """شبكة عصبية تلافيفية (CNN)"""
    
    def __init__(self, input_shape: Tuple, num_classes: int):
        self.input_shape = input_shape
        self.num_classes = num_classes
        self.filters = []
        self.kernels = []
    
    def create_filter(self, size: int, num_filters: int):
        """إنشاء مرشحات"""
        self.filters.append(np.random.randn(size, size, num_filters) * 0.01)
    
    def convolve(self, image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
        """عملية التلافيف"""
        
        kernel_size = kernel.shape[0]
        output_size = image.shape[0] - kernel_size + 1
        output = np.zeros((output_size, output_size))
        
        for i in range(output_size):
            for j in range(output_size):
                patch = image[i:i+kernel_size, j:j+kernel_size]
                output[i, j] = np.sum(patch * kernel)
        
        return output
    
    def pool(self, image: np.ndarray, pool_size: int = 2) -> np.ndarray:
        """عملية Pooling"""
        
        output_size = image.shape[0] // pool_size
        output = np.zeros((output_size, output_size))
        
        for i in range(output_size):
            for j in range(output_size):
                patch = image[i*pool_size:(i+1)*pool_size, j*pool_size:(j+1)*pool_size]
                output[i, j] = np.max(patch)
        
        return output


class NaturalLanguageProcessor:
    """معالج اللغة الطبيعية"""
    
    def __init__(self):
        self.vocabulary = {}
        self.embeddings = {}
        self.word_count = 0
    
    def tokenize(self, text: str) -> List[str]:
        """تقسيم النص إلى كلمات"""
        return text.lower().split()
    
    def build_vocabulary(self, texts: List[str]):
        """بناء قاموس"""
        
        for text in texts:
            tokens = self.tokenize(text)
            for token in tokens:
                if token not in self.vocabulary:
                    self.vocabulary[token] = self.word_count
                    self.word_count += 1
    
    def embed_text(self, text: str) -> np.ndarray:
        """تحويل النص إلى تمثيل رقمي"""
        
        tokens = self.tokenize(text)
        embedding = np.zeros(len(self.vocabulary))
        
        for token in tokens:
            if token in self.vocabulary:
                embedding[self.vocabulary[token]] += 1
        
        # تطبيع
        if np.sum(embedding) > 0:
            embedding = embedding / np.sum(embedding)
        
        return embedding


class DeepLearningEngine:
    """محرك التعلم العميق الرئيسي"""
    
    def __init__(self):
        self.neural_network = NeuralNetwork(784, 128, 10)
        self.reinforcement_learner = ReinforcementLearner(100, 10)
        self.cnn = ConvolutionalNeuralNetwork((28, 28), 10)
        self.nlp = NaturalLanguageProcessor()
        
        self.training_history = []
        self.performance_metrics = {
            'accuracy': 0.0,
            'loss': 0.0,
            'episodes': 0
        }
    
    async def train_neural_network(self, X_train: np.ndarray, y_train: np.ndarray, epochs: int = 100):
        """تدريب الشبكة العصبية"""
        
        logger.info(f"🧠 بدء تدريب الشبكة العصبية ({epochs} حقبة)")
        
        for epoch in range(epochs):
            # المسار الأمامي
            output = self.neural_network.forward(X_train)
            
            # حساب الخسارة
            loss = -np.mean(y_train * np.log(output + 1e-8))
            
            # حساب التدرج
            dZ2 = output - y_train
            
            # المسار الخلفي
            self.neural_network.backward(dZ2)
            
            # تسجيل
            self.training_history.append({
                'epoch': epoch,
                'loss': loss,
                'timestamp': datetime.now().isoformat()
            })
            
            if (epoch + 1) % 10 == 0:
                logger.info(f"  الحقبة {epoch + 1}/{epochs} - الخسارة: {loss:.4f}")
        
        logger.info("✅ انتهى التدريب")
    
    async def train_reinforcement_learning(self, episodes: int = 1000):
        """تدريب التعلم المعزز"""
        
        logger.info(f"🎮 بدء تدريب التعلم المعزز ({episodes} حلقة)")
        
        for episode in range(episodes):
            state = 0
            done = False
            total_reward = 0
            
            while not done:
                # اختيار إجراء
                action = self.reinforcement_learner.select_action(state)
                
                # محاكاة البيئة
                next_state = (state + action) % self.reinforcement_learner.state_size
                reward = 1.0 if next_state > state else -0.1
                done = next_state == 99
                
                # التعلم
                self.reinforcement_learner.learn(state, action, reward, next_state, done)
                
                total_reward += reward
                state = next_state
            
            self.performance_metrics['episodes'] = episode + 1
            
            if (episode + 1) % 100 == 0:
                logger.info(f"  الحلقة {episode + 1}/{episodes} - المكافأة: {total_reward:.2f}")
        
        logger.info("✅ انتهى التدريب")
    
    async def process_image(self, image: np.ndarray) -> Dict:
        """معالجة الصورة"""
        
        logger.info("📷 معالجة الصورة")
        
        try:
            # تطبيق الفلاتر
            filtered = image.copy()
            for i, filter_bank in enumerate(self.cnn.filters):
                for j in range(filter_bank.shape[2]):
                    kernel = filter_bank[:, :, j]
                    filtered = self.cnn.convolve(filtered, kernel)
            
            # Pooling
            pooled = self.cnn.pool(filtered)
            
            return {
                'status': 'success',
                'original_shape': image.shape,
                'processed_shape': pooled.shape,
                'features_extracted': pooled.flatten().shape[0]
            }
        
        except Exception as e:
            logger.error(f"خطأ في معالجة الصورة: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def process_text(self, text: str) -> Dict:
        """معالجة النص"""
        
        logger.info(f"📝 معالجة النص: {text[:50]}...")
        
        try:
            # بناء القاموس (إذا لم يكن موجوداً)
            if not self.nlp.vocabulary:
                self.nlp.build_vocabulary([text])
            
            # تحويل النص
            embedding = self.nlp.embed_text(text)
            
            return {
                'status': 'success',
                'text': text,
                'embedding_size': embedding.shape[0],
                'tokens': len(self.nlp.tokenize(text))
            }
        
        except Exception as e:
            logger.error(f"خطأ في معالجة النص: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def submit_task(self, task: Dict) -> Dict:
        """تقديم مهمة"""
        
        if task.get('type') == 'train_nn':
            # تدريب الشبكة العصبية
            X = np.random.randn(100, 784)
            y = np.eye(10)[np.random.randint(0, 10, 100)]
            
            await self.train_neural_network(X, y, epochs=task.get('epochs', 100))
            
            return {
                'status': 'completed',
                'type': 'neural_network',
                'history': self.training_history[-10:]
            }
        
        elif task.get('type') == 'train_rl':
            # تدريب التعلم المعزز
            await self.train_reinforcement_learning(episodes=task.get('episodes', 1000))
            
            return {
                'status': 'completed',
                'type': 'reinforcement_learning',
                'metrics': self.performance_metrics
            }
        
        elif task.get('type') == 'process_image':
            # معالجة الصورة
            image = np.random.randn(28, 28)
            return await self.process_image(image)
        
        elif task.get('type') == 'process_text':
            # معالجة النص
            return await self.process_text(task.get('text', ''))
        
        return {'status': 'error', 'message': 'نوع مهمة غير معروف'}
    
    def get_metrics(self) -> Dict:
        """الحصول على المقاييس"""
        return self.performance_metrics


# مثال على الاستخدام
async def main():
    engine = DeepLearningEngine()
    
    # تدريب الشبكة العصبية
    result1 = await engine.submit_task({
        'type': 'train_nn',
        'epochs': 50
    })
    print(f"نتيجة NN: {result1}")
    
    # تدريب التعلم المعزز
    result2 = await engine.submit_task({
        'type': 'train_rl',
        'episodes': 500
    })
    print(f"نتيجة RL: {result2}")
    
    # معالجة النص
    result3 = await engine.submit_task({
        'type': 'process_text',
        'text': 'مرحبا بك في محرك التعلم العميق'
    })
    print(f"نتيجة NLP: {result3}")


if __name__ == "__main__":
    asyncio.run(main())
