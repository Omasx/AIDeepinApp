"""
🎓 Real Training System - نظام التدريب الفعلي المتقدم
تدريب النماذج بشكل احترافي مع معالجة البيانات والمراقبة

يتضمن:
- معالجة البيانات الفعلية
- تدريب متقدم
- Callbacks ومراقبة
- حفظ واستعادة النقاط
- معايرة النماذج
"""

import numpy as np
import logging
from typing import Dict, Any, Optional, Tuple, List
from dataclasses import dataclass
from datetime import datetime
import json
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import callbacks
    TF_AVAILABLE = True
except ImportError:
    logger.warning("⚠️ TensorFlow غير متوفر")
    TF_AVAILABLE = False


@dataclass
class TrainingConfig:
    """إعدادات التدريب"""
    batch_size: int = 32
    epochs: int = 50
    learning_rate: float = 0.001
    validation_split: float = 0.2
    early_stopping_patience: int = 5
    reduce_lr_patience: int = 3
    checkpoint_dir: str = "./checkpoints"


class RealTrainingSystem:
    """نظام التدريب الفعلي"""
    
    def __init__(self, config: TrainingConfig = None):
        self.config = config or TrainingConfig()
        self.tf_available = TF_AVAILABLE
        self.training_history = {}
        self.best_models = {}
        
        # إنشاء مجلد نقاط التفتيش
        os.makedirs(self.config.checkpoint_dir, exist_ok=True)
        
        logger.info(f"🎓 تهيئة نظام التدريب - TensorFlow: {'متاح' if self.tf_available else 'غير متاح'}")
    
    def prepare_data(self, X: np.ndarray, y: np.ndarray, 
                    validation_split: float = None) -> Tuple[Dict, Dict]:
        """تحضير البيانات للتدريب"""
        
        logger.info("📊 تحضير البيانات")
        
        validation_split = validation_split or self.config.validation_split
        
        # تقسيم البيانات
        num_samples = len(X)
        num_train = int(num_samples * (1 - validation_split))
        
        indices = np.random.permutation(num_samples)
        train_indices = indices[:num_train]
        val_indices = indices[num_train:]
        
        X_train, y_train = X[train_indices], y[train_indices]
        X_val, y_val = X[val_indices], y[val_indices]
        
        # تطبيع البيانات
        X_mean = X_train.mean()
        X_std = X_train.std()
        
        X_train = (X_train - X_mean) / (X_std + 1e-7)
        X_val = (X_val - X_mean) / (X_std + 1e-7)
        
        logger.info(f"✅ تم تحضير البيانات:")
        logger.info(f"   - عينات التدريب: {len(X_train)}")
        logger.info(f"   - عينات التحقق: {len(X_val)}")
        
        return {
            'X_train': X_train,
            'y_train': y_train,
            'X_val': X_val,
            'y_val': y_val
        }, {
            'mean': X_mean,
            'std': X_std
        }
    
    def create_callbacks(self, model_name: str) -> List[Any]:
        """إنشاء Callbacks للتدريب"""
        
        if not self.tf_available:
            return []
        
        logger.info(f"🔧 إنشاء Callbacks لـ {model_name}")
        
        checkpoint_path = os.path.join(
            self.config.checkpoint_dir,
            f"{model_name}_best.h5"
        )
        
        callback_list = [
            # حفظ أفضل نموذج
            callbacks.ModelCheckpoint(
                checkpoint_path,
                monitor='val_loss',
                save_best_only=True,
                verbose=1
            ),
            
            # إيقاف مبكر
            callbacks.EarlyStopping(
                monitor='val_loss',
                patience=self.config.early_stopping_patience,
                verbose=1,
                restore_best_weights=True
            ),
            
            # تقليل معدل التعلم
            callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=self.config.reduce_lr_patience,
                min_lr=1e-7,
                verbose=1
            ),
            
            # تسجيل الأحداث
            callbacks.CSVLogger(
                os.path.join(self.config.checkpoint_dir, f"{model_name}_log.csv")
            ),
            
            # معدل التعلم الديناميكي
            callbacks.LambdaCallback(
                on_epoch_end=self._on_epoch_end
            )
        ]
        
        return callback_list
    
    def _on_epoch_end(self, epoch: int, logs: Dict = None):
        """معالج نهاية الحقبة"""
        
        if logs is None:
            return
        
        if epoch % 10 == 0:
            logger.info(f"📈 الحقبة {epoch}: loss={logs.get('loss', 0):.4f}, "
                       f"val_loss={logs.get('val_loss', 0):.4f}")
    
    def train_model(self, model: Any, model_name: str, 
                   data: Dict, epochs: int = None,
                   verbose: int = 1) -> Dict[str, Any]:
        """تدريب النموذج"""
        
        if not self.tf_available:
            return {'status': 'error', 'message': 'TensorFlow غير متاح'}
        
        logger.info(f"🎓 بدء تدريب {model_name}")
        
        epochs = epochs or self.config.epochs
        
        try:
            # الحصول على البيانات
            X_train = data['X_train']
            y_train = data['y_train']
            X_val = data['X_val']
            y_val = data['y_val']
            
            # إنشاء Callbacks
            callback_list = self.create_callbacks(model_name)
            
            # التدريب
            start_time = datetime.now()
            
            history = model.fit(
                X_train, y_train,
                batch_size=self.config.batch_size,
                epochs=epochs,
                validation_data=(X_val, y_val),
                callbacks=callback_list,
                verbose=verbose
            )
            
            training_time = (datetime.now() - start_time).total_seconds()
            
            # حفظ السجل
            self.training_history[model_name] = {
                'history': history.history,
                'training_time': training_time,
                'epochs': epochs,
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"✅ تم تدريب {model_name} في {training_time:.2f} ثانية")
            
            return {
                'status': 'success',
                'model': model_name,
                'epochs': epochs,
                'training_time': training_time,
                'final_loss': float(history.history['loss'][-1]),
                'final_val_loss': float(history.history['val_loss'][-1]),
                'history': history.history
            }
        
        except Exception as e:
            logger.error(f"❌ خطأ في التدريب: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def evaluate_model(self, model: Any, model_name: str,
                      X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, Any]:
        """تقييم النموذج"""
        
        if not self.tf_available:
            return {'status': 'error', 'message': 'TensorFlow غير متاح'}
        
        logger.info(f"📊 تقييم نموذج {model_name}")
        
        try:
            loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
            
            # حساب مقاييس إضافية
            predictions = model.predict(X_test, verbose=0)
            
            logger.info(f"✅ نتائج التقييم:")
            logger.info(f"   - الخسارة: {loss:.4f}")
            logger.info(f"   - الدقة: {accuracy:.4f}")
            
            return {
                'status': 'success',
                'model': model_name,
                'loss': float(loss),
                'accuracy': float(accuracy),
                'predictions_shape': predictions.shape
            }
        
        except Exception as e:
            logger.error(f"❌ خطأ في التقييم: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def hyperparameter_tuning(self, model_builder, X: np.ndarray, y: np.ndarray,
                             param_grid: Dict) -> Dict[str, Any]:
        """ضبط المعاملات الفائقة"""
        
        if not self.tf_available:
            return {'status': 'error', 'message': 'TensorFlow غير متاح'}
        
        logger.info("🔧 بدء ضبط المعاملات الفائقة")
        
        # تحضير البيانات
        data, _ = self.prepare_data(X, y)
        
        best_result = None
        best_params = None
        results = []
        
        # البحث الشبكي
        param_combinations = self._generate_param_combinations(param_grid)
        
        for i, params in enumerate(param_combinations):
            logger.info(f"\n🔍 المحاولة {i+1}/{len(param_combinations)}: {params}")
            
            try:
                # بناء النموذج
                model = model_builder(params)
                
                # التدريب
                history = model.fit(
                    data['X_train'], data['y_train'],
                    batch_size=self.config.batch_size,
                    epochs=10,  # حقب قليلة للاختبار السريع
                    validation_data=(data['X_val'], data['y_val']),
                    verbose=0
                )
                
                # التقييم
                val_loss = history.history['val_loss'][-1]
                
                result = {
                    'params': params,
                    'val_loss': float(val_loss),
                    'history': history.history
                }
                
                results.append(result)
                
                logger.info(f"✅ val_loss: {val_loss:.4f}")
                
                # تحديث الأفضل
                if best_result is None or val_loss < best_result['val_loss']:
                    best_result = result
                    best_params = params
            
            except Exception as e:
                logger.error(f"❌ خطأ: {e}")
                continue
        
        logger.info(f"\n🏆 أفضل المعاملات: {best_params}")
        
        return {
            'status': 'success',
            'best_params': best_params,
            'best_val_loss': best_result['val_loss'] if best_result else None,
            'total_trials': len(results),
            'successful_trials': len([r for r in results if r])
        }
    
    def _generate_param_combinations(self, param_grid: Dict) -> List[Dict]:
        """توليد مجموعات المعاملات"""
        
        import itertools
        
        keys = param_grid.keys()
        values = param_grid.values()
        
        combinations = []
        for combination in itertools.product(*values):
            combinations.append(dict(zip(keys, combination)))
        
        return combinations
    
    def save_training_log(self, model_name: str, path: str) -> Dict[str, Any]:
        """حفظ سجل التدريب"""
        
        if model_name not in self.training_history:
            return {'status': 'error', 'message': f'لا يوجد سجل لـ {model_name}'}
        
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self.training_history[model_name], f, indent=2, ensure_ascii=False)
            
            logger.info(f"💾 تم حفظ السجل: {path}")
            
            return {'status': 'success', 'path': path}
        
        except Exception as e:
            logger.error(f"❌ خطأ: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def get_training_summary(self) -> Dict[str, Any]:
        """الحصول على ملخص التدريب"""
        
        summary = {
            'total_models_trained': len(self.training_history),
            'models': {}
        }
        
        for model_name, history in self.training_history.items():
            summary['models'][model_name] = {
                'epochs': history.get('epochs', 0),
                'training_time': history.get('training_time', 0),
                'timestamp': history.get('timestamp', '')
            }
        
        return summary


# مثال على الاستخدام
async def main():
    """البرنامج الرئيسي"""
    
    print("\n" + "="*70)
    print("🎓 نظام التدريب الفعلي")
    print("="*70 + "\n")
    
    # إنشاء نظام التدريب
    trainer = RealTrainingSystem()
    
    # توليد بيانات وهمية للاختبار
    print("📊 توليد بيانات الاختبار...\n")
    
    X = np.random.randn(1000, 28, 28, 1).astype(np.float32)
    y = np.random.randint(0, 10, 1000)
    y = keras.utils.to_categorical(y, 10)
    
    # تحضير البيانات
    data, normalization = trainer.prepare_data(X, y)
    
    print(f"\n✅ تم تحضير البيانات")
    print(f"   - معامل التطبيع: mean={normalization['mean']:.4f}, std={normalization['std']:.4f}")
    
    # عرض ملخص التدريب
    print("\n" + "="*70)
    print("✅ نظام التدريب جاهز للاستخدام!")
    print("="*70 + "\n")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
