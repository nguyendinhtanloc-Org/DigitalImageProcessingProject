# Model Service - Python Flask API

**Shared by:** Quốc Anh (CNN) & Tấn Lộc (ResNet50)

## Setup môi trường

```bash
cd model-service

# Tạo môi trường ảo
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Cài packages
pip install -r requirements.txt
```

## Cấu trúc

```
model-service/
├── models/
│   ├── cnn_best.h5              # CNN từ Quốc Anh
│   └── resnet50_best.h5         # ResNet50 từ Tấn Lộc
├── app/
│   ├── __init__.py
│   ├── app.py                   # Flask main
│   ├── routes/
│   │   ├── predict.py          # Prediction endpoints
│   │   └── health.py           # Health check
│   ├── services/
│   │   ├── cnn_service.py      # CNN inference
│   │   ├── resnet_service.py   # ResNet inference
│   │   └── image_processor.py  # Image preprocessing
│   └── utils/
│       └── validators.py
├── requirements.txt
├── Dockerfile
└── README.md
```

## API Endpoints

### 1. Predict with CNN
```bash
POST /predict/cnn
Content-Type: multipart/form-data
Body: file=<image>

Response:
{
  "prediction": "PNEUMONIA",
  "confidence": 0.9542
}
```

### 2. Predict with ResNet50
```bash
POST /predict/resnet50
Content-Type: multipart/form-data
Body: file=<image>

Response:
{
  "prediction": "NORMAL",
  "confidence": 0.8734
}
```

### 3. Health Check
```bash
GET /health

Response:
{
  "status": "healthy",
  "models_loaded": ["cnn", "resnet50"]
}
```

## Công việc

### Quốc Anh (CNN)
- [ ] Export CNN model (.h5)
- [ ] Viết `cnn_service.py`
- [ ] Test inference locally
- [ ] Bàn giao model file

### Tấn Lộc (ResNet50)
- [ ] Export ResNet50 model (.h5)
- [ ] Viết `resnet_service.py`
- [ ] Test inference locally
- [ ] Bàn giao model file

### Shared (ai làm cũng được)
- [ ] Setup Flask app
- [ ] Image preprocessing pipeline
- [ ] Error handling
- [ ] Docker container

## Tech Stack
- Python 3.8+
- Flask
- TensorFlow/Keras
- OpenCV
- Pillow

## Run local
```bash
cd model-service

# Kích hoạt môi trường ảo
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Run Flask
python app/app.py
# Server: http://localhost:5000
```

## requirements.txt
```txt
flask==3.0.0
tensorflow==2.15.0
keras==2.15.0
opencv-python==4.8.1
pillow==10.0.0
numpy==1.24.3
```

## Docker
```bash
docker build -t pneumonia-model-service .
docker run -p 5000:5000 pneumonia-model-service
```
