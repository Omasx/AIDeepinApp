"""
🧠 Real RNN/LSTM Models - نماذج الشبكات العصبية المتكررة الحقيقية
معالجة النصوص والتسلسلات بشكل احترافي

يتضمن:
- نموذج LSTM أساسي
- نموذج Bidirectional LSTM
- نموذج GRU
- نموذج Attention
- معالجة النصوص الفعلية
"""

import numpy as np
import logging
from typing import Tuple, List, Dict, Any, Optional
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers, models
    TF_AVAILABLE = True
except ImportError:
    logger.warning("⚠️ TensorFlow غير متوفر")
    TF_AVAILABLE = False


@dataclass
class RNNConfig:
    """إعدادات نماذج RNN"""
    vocab_size: int = 10000
    embedding_dim: int = 128
    max_length: int = 100
    lstm_units: int = 64
    dropout_rate: float = 0.5
    batch_size: int = 32
    epochs: int = 10


class RealRNNModels:
    """فئة نماذج RNN/LSTM الحقيقية"""
    
    def __init__(self, config: RNNConfig = None):
        self.config = config or RNNConfig()
        self.models = {}
        self.tokenizer = None
        self.tf_available = TF_AVAILABLE
        
        logger.info(f"🧠 تهيئة نماذج RNN - TensorFlow: {'متاح' if self.tf_available else 'غير متاح'}")
    
    def build_simple_lstm(self, name: str = "simple_lstm") -> Optional[Any]:
        """بناء نموذج LSTM بسيط"""
        
        if not self.tf_available:
            return None
        
        logger.info(f"🔨 بناء نموذج {name}")
        
        model = models.Sequential([
            # طبقة التضمين
            layers.Embedding(self.config.vocab_size, self.config.embedding_dim,
                            input_length=self.config.max_length),
            
            # طبقة LSTM الأولى
            layers.LSTM(self.config.lstm_units, return_sequences=True),
            layers.Dropout(self.config.dropout_rate),
            
            # طبقة LSTM الثانية
            layers.LSTM(self.config.lstm_units),
            layers.Dropout(self.config.dropout_rate),
            
            # طبقات كاملة
            layers.Dense(64, activation='relu'),
            layers.Dropout(self.config.dropout_rate),
            layers.Dense(1, activation='sigmoid')  # للتصنيف الثنائي
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        self.models[name] = model
        logger.info(f"✅ تم بناء {name}")
        
        return model
    
    def build_bidirectional_lstm(self, name: str = "bidirectional_lstm") -> Optional[Any]:
        """بناء نموذج Bidirectional LSTM"""
        
        if not self.tf_available:
            return None
        
        logger.info(f"🔨 بناء نموذج {name}")
        
        model = models.Sequential([
            # طبقة التضمين
            layers.Embedding(self.config.vocab_size, self.config.embedding_dim,
                            input_length=self.config.max_length),
            
            # طبقة Bidirectional LSTM
            layers.Bidirectional(
                layers.LSTM(self.config.lstm_units, return_sequences=True)
            ),
            layers.Dropout(self.config.dropout_rate),
            
            # طبقة Bidirectional LSTM الثانية
            layers.Bidirectional(
                layers.LSTM(self.config.lstm_units)
            ),
            layers.Dropout(self.config.dropout_rate),
            
            # طبقات كاملة
            layers.Dense(128, activation='relu'),
            layers.Dropout(self.config.dropout_rate),
            layers.Dense(64, activation='relu'),
            layers.Dropout(self.config.dropout_rate),
            layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        self.models[name] = model
        logger.info(f"✅ تم بناء {name}")
        
        return model
    
    def build_gru_model(self, name: str = "gru_model") -> Optional[Any]:
        """بناء نموذج GRU"""
        
        if not self.tf_available:
            return None
        
        logger.info(f"🔨 بناء نموذج {name}")
        
        model = models.Sequential([
            # طبقة التضمين
            layers.Embedding(self.config.vocab_size, self.config.embedding_dim,
                            input_length=self.config.max_length),
            
            # طبقة GRU الأولى
            layers.GRU(self.config.lstm_units, return_sequences=True),
            layers.Dropout(self.config.dropout_rate),
            
            # طبقة GRU الثانية
            layers.GRU(self.config.lstm_units),
            layers.Dropout(self.config.dropout_rate),
            
            # طبقات كاملة
            layers.Dense(64, activation='relu'),
            layers.Dropout(self.config.dropout_rate),
            layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        self.models[name] = model
        logger.info(f"✅ تم بناء {name}")
        
        return model
    
    def build_attention_model(self, name: str = "attention_model") -> Optional[Any]:
        """بناء نموذج مع آلية Attention"""
        
        if not self.tf_available:
            return None
        
        logger.info(f"🔨 بناء نموذج {name} مع Attention")
        
        # المدخلات
        inputs = keras.Input(shape=(self.config.max_length,))
        
        # طبقة التضمين
        x = layers.Embedding(self.config.vocab_size, self.config.embedding_dim)(inputs)
        
        # طبقة LSTM
        x = layers.LSTM(self.config.lstm_units, return_sequences=True)(x)
        x = layers.Dropout(self.config.dropout_rate)(x)
        
        # آلية Attention
        attention = layers.MultiHeadAttention(
            num_heads=4,
            key_dim=self.config.lstm_units // 4
        )(x, x)
        
        # دمج مع المسار الأصلي
        x = layers.Add()([x, attention])
        x = layers.LayerNormalization()(x)
        
        # طبقة LSTM أخرى
        x = layers.LSTM(self.config.lstm_units)(x)
        x = layers.Dropout(self.config.dropout_rate)(x)
        
        # طبقات كاملة
        x = layers.Dense(64, activation='relu')(x)
        x = layers.Dropout(self.config.dropout_rate)(x)
        outputs = layers.Dense(1, activation='sigmoid')(x)
        
        model = models.Model(inputs=inputs, outputs=outputs)
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        self.models[name] = model
        logger.info(f"✅ تم بناء {name}")
        
        return model
    
    def build_text_generation_model(self, name: str = "text_generation") -> Optional[Any]:
        """بناء نموذج لتوليد النصوص"""
        
        if not self.tf_available:
            return None
        
        logger.info(f"🔨 بناء نموذج {name}")
        
        model = models.Sequential([
            # طبقة التضمين
            layers.Embedding(self.config.vocab_size, self.config.embedding_dim,
                            input_length=self.config.max_length - 1),
            
            # طبقات LSTM
            layers.LSTM(128, return_sequences=True),
            layers.Dropout(0.3),
            
            layers.LSTM(128),
            layers.Dropout(0.3),
            
            # طبقات كاملة
            layers.Dense(256, activation='relu'),
            layers.Dropout(0.3),
            
            # إخراج: توقع الكلمة التالية
            layers.Dense(self.config.vocab_size, activation='softmax')
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.models[name] = model
        logger.info(f"✅ تم بناء {name}")
        
        return model
    
    def build_sequence_to_sequence(self, name: str = "seq2seq") -> Optional[Any]:
        """بناء نموذج Sequence-to-Sequence"""
        
        if not self.tf_available:
            return None
        
        logger.info(f"🔨 بناء نموذج {name}")
        
        # المشفر (Encoder)
        encoder_inputs = keras.Input(shape=(self.config.max_length,))
        encoder_embedding = layers.Embedding(self.config.vocab_size, 
                                            self.config.embedding_dim)(encoder_inputs)
        encoder_lstm = layers.LSTM(self.config.lstm_units, 
                                   return_state=True)
        encoder_outputs, state_h, state_c = encoder_lstm(encoder_embedding)
        encoder_states = [state_h, state_c]
        
        # فك التشفير (Decoder)
        decoder_inputs = keras.Input(shape=(self.config.max_length,))
        decoder_embedding = layers.Embedding(self.config.vocab_size,
                                            self.config.embedding_dim)(decoder_inputs)
        decoder_lstm = layers.LSTM(self.config.lstm_units, return_sequences=True,
                                   return_state=True)
        decoder_outputs, _, _ = decoder_lstm(decoder_embedding, 
                                            initial_state=encoder_states)
        decoder_dense = layers.Dense(self.config.vocab_size, activation='softmax')
        decoder_outputs = decoder_dense(decoder_outputs)
        
        # النموذج الكامل
        model = models.Model([encoder_inputs, decoder_inputs], decoder_outputs)
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.models[name] = model
        logger.info(f"✅ تم بناء {name}")
        
        return model
    
    def train_model(self, model_name: str, X_train: np.ndarray, y_train: np.ndarray,
                   X_val: np.ndarray = None, y_val: np.ndarray = None,
                   epochs: int = None) -> Dict[str, Any]:
        """تدريب النموذج"""
        
        if not self.tf_available:
            return {'status': 'error', 'message': 'TensorFlow غير متاح'}
        
        if model_name not in self.models:
            return {'status': 'error', 'message': f'النموذج {model_name} غير موجود'}
        
        model = self.models[model_name]
        epochs = epochs or self.config.epochs
        
        logger.info(f"🎓 تدريب نموذج {model_name}")
        
        try:
            history = model.fit(
                X_train, y_train,
                batch_size=self.config.batch_size,
                epochs=epochs,
                validation_data=(X_val, y_val) if X_val is not None else None,
                verbose=1
            )
            
            return {
                'status': 'success',
                'model': model_name,
                'epochs': epochs,
                'history': history.history
            }
        
        except Exception as e:
            logger.error(f"❌ خطأ: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def predict(self, model_name: str, X: np.ndarray) -> Dict[str, Any]:
        """التنبؤ"""
        
        if not self.tf_available:
            return {'status': 'error', 'message': 'TensorFlow غير متاح'}
        
        if model_name not in self.models:
            return {'status': 'error', 'message': f'النموذج {model_name} غير موجود'}
        
        try:
            model = self.models[model_name]
            predictions = model.predict(X, verbose=0)
            
            return {
                'status': 'success',
                'predictions': predictions.tolist(),
                'shape': predictions.shape
            }
        
        except Exception as e:
            logger.error(f"❌ خطأ: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """الحصول على معلومات النموذج"""
        
        if model_name not in self.models:
            return {'status': 'error', 'message': f'النموذج {model_name} غير موجود'}
        
        if not self.tf_available:
            return {'status': 'success', 'message': 'TensorFlow غير متاح'}
        
        try:
            model = self.models[model_name]
            
            return {
                'status': 'success',
                'model': model_name,
                'num_layers': len(model.layers),
                'total_params': model.count_params(),
                'input_shape': str(model.input_shape),
                'output_shape': str(model.output_shape)
            }
        
        except Exception as e:
            return {'status': 'error', 'message': str(e)}


# مثال على الاستخدام
async def main():
    """البرنامج الرئيسي"""
    
    print("\n" + "="*70)
    print("🧠 نماذج RNN/LSTM حقيقية")
    print("="*70 + "\n")
    
    # إنشاء النماذج
    rnn = RealRNNModels()
    
    # بناء النماذج
    print("🔨 بناء النماذج...\n")
    
    rnn.build_simple_lstm("simple_lstm")
    rnn.build_bidirectional_lstm("bidirectional_lstm")
    rnn.build_gru_model("gru_model")
    rnn.build_attention_model("attention_model")
    rnn.build_text_generation_model("text_generation")
    rnn.build_sequence_to_sequence("seq2seq")
    
    # عرض معلومات النماذج
    print("\n📊 معلومات النماذج:\n")
    
    for model_name in ["simple_lstm", "bidirectional_lstm", "gru_model", 
                       "attention_model", "text_generation", "seq2seq"]:
        info = rnn.get_model_info(model_name)
        print(f"✅ {model_name}: {info}")
    
    print("\n" + "="*70)
    print("✅ تم بناء جميع نماذج RNN بنجاح!")
    print("="*70 + "\n")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
