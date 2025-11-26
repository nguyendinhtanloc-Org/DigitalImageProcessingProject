# Project Structure Summary

## Cấu trúc đã tạo

```
DigitalImageProcessingProject/
│
├── backend/
│   ├── src/main/java/com/pneumonia/     # Java source code
│   ├── src/main/resources/              # Config files
│   ├── src/test/                        # Tests
│   ├── TASKS.md                         # Quang Duy's tasks
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── components/                  # React components
│   │   ├── pages/                       # Pages
│   │   ├── services/                    # API services
│   │   └── utils/                       # Utilities
│   ├── public/
│   ├── TASKS.md                         # Quốc Anh's tasks
│   └── README.md
│
├── model-service/                       # Flask API cho models
│   └── README.md
│
├── notebooks/                           # Kaggle notebooks
│   ├── CNN.ipynb                        # Quốc Anh
│   ├── ResNet.ipynb                     # Tấn Lộc
│   ├── evaluation/
│   ├── comparison/
│   └── README.md
│
├── data/
│   ├── preprocessing-scripts/           # Python scripts - Quang Duy
│   ├── reports/                         # Báo cáo tiền xử lý
│   ├── TASKS_QUANGDUY.md               # Chi tiết công việc
│   └── README.md
│
├── models/                              # Saved models (.h5)
│   └── README.md
│
├── deployment/                          # Docker deployment - Tấn Lộc
│   ├── docker-compose.yml
│   └── README.md
│
├── docs/
│   └── images/
│
├── TASKS_TANLOC.md                     # Chi tiết công việc Tấn Lộc
├── CONTRIBUTING.md
├── .gitignore
└── README.md
```

## Files quan trọng đã tạo

### Phân công công việc
1. **backend/TASKS.md** - Nguyễn Văn Quang Duy (Backend API)
2. **frontend/TASKS.md** - Nguyễn Đặng Quốc Anh (Frontend & CNN)
3. **data/TASKS_QUANGDUY.md** - Nguyễn Văn Quang Duy (Data Preprocessing)
4. **TASKS_TANLOC.md** - Nguyễn Đình Tấn Lộc (ResNet50 & Integration)

### Technical Documentation
1. **model-service/README.md** - Flask API cho model inference
2. **notebooks/README.md** - Hướng dẫn training trên Kaggle
3. **deployment/README.md** - Docker deployment guide
4. **deployment/docker-compose.yml** - Container orchestration

### Main README
- **README.md** - Đã cập nhật với cấu trúc mới và phân công chi tiết

## Kiến trúc hệ thống

```
User Browser
    ↓
Frontend (React:3000)
    ↓
Backend (Spring Boot:8080)
    ↓
Model Service (Flask:5000)
    ├── CNN Model
    └── ResNet50 Model
```

## Workflow tổng thể

### Phase 1: Data Preparation (Quang Duy)
1. Download dataset
2. Data cleaning
3. Preprocessing
4. Augmentation
5. Split dataset
→ Bàn giao cho Quốc Anh & Tấn Lộc

### Phase 2: Model Development (Parallel)
**Quốc Anh:**
- Xây dựng CNN
- Training trên Kaggle
- Export model

**Tấn Lộc:**
- Fine-tune ResNet50
- Training trên Kaggle
- Export model

### Phase 3: Backend Development (Quang Duy)
- Spring Boot API
- Image upload handling
- Model service integration
→ Bàn giao API cho Tấn Lộc

### Phase 4: Frontend Development (Quốc Anh)
- React components
- UI/UX design
- Mock data testing
→ Bàn giao UI cho Tấn Lộc

### Phase 5: Integration (Tấn Lộc)
- Connect Frontend ↔ Backend
- End-to-end testing
- Bug fixing

### Phase 6: Comparison & Deployment (Tấn Lộc)
- Model comparison analysis
- Docker setup
- Full deployment

## Next Steps

### Quang Duy
1. Đọc `data/TASKS_QUANGDUY.md`
2. Đọc `backend/TASKS.md`
3. Bắt đầu với data preprocessing

### Quốc Anh
1. Đọc `frontend/TASKS.md`
2. Đọc `notebooks/README.md`
3. Setup React project & CNN notebook

### Tấn Lộc
1. Đọc `TASKS_TANLOC.md`
2. Đọc `notebooks/README.md`
3. Chuẩn bị ResNet50 notebook

## Quick Start Commands

### Backend
```bash
cd backend
mvn spring-boot:run
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Model Service
```bash
cd model-service
pip install -r requirements.txt
python app/app.py
```

### Full Stack (Docker)
```bash
cd deployment
docker-compose up --build
```

## Important Notes

1. **Dataset không commit lên Git** - quá lớn
2. **Model files không commit** - quá lớn, share qua Google Drive
3. **Upload temp files** - tự động xóa sau predict
4. **History** - lưu trong localStorage, không cần database
5. **Authentication** - không cần login
6. **CORS** - Backend phải config cho frontend

## Support

Nếu có thắc mắc về:
- **Backend & Data:** Hỏi Quang Duy
- **Frontend & CNN:** Hỏi Quốc Anh
- **ResNet50 & Integration:** Hỏi Tấn Lộc
- **General:** Tham khảo CONTRIBUTING.md
