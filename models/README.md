# Models Directory

## Trained Models

- `cnn_best.h5` - CNN model (Quốc Anh, ~88-92% accuracy)
- `resnet50_best.h5` - ResNet50 model (Tấn Lộc, ~92-96% accuracy)

## Sử dụng

```python
import tensorflow as tf

# Load model
model = tf.keras.models.load_model('models/cnn_best.h5')

# Predict
prediction = model.predict(image_array)
```

## Lưu ý

- File `.h5` dùng Git LFS (quá lớn để commit thường)
- Hoặc chia sẻ qua Google Drive
