# Hướng dẫn bắt đầu dự án

**Đọc file này TRƯỚC KHI BẮT ĐẦU CODE!**

## Bước 1: Hiểu cấu trúc dự án

```
GETTING_STARTED.md  ← Bạn đang đọc file này
    ↓
README.md           ← Tổng quan dự án
    ↓
TIMELINE.md         ← Timeline 3 tuần (ai làm gì, khi nào)
    ↓
CONTRIBUTING.md     ← Quy tắc commit, branch, code
    ↓
[Task file của bạn] ← Chi tiết công việc theo iteration
```

## Bước 2: Đọc theo thứ tự này

### 1. Đọc README.md (5 phút)
- Hiểu dự án làm gì
- Xem kiến trúc hệ thống
- Biết tech stack dùng gì

### 2. Đọc TIMELINE.md (10 phút)
- Xem timeline 3 tuần
- Tìm phần công việc của mình
- Note deadline từng iteration

### 3. Đọc CONTRIBUTING.md (10 phút)
- Học cách tạo branch
- Học cách commit message
- Hiểu quy trình Git Flow

### 4. Đọc task file ITERATION hiện tại (10 phút)
- **Iteration 1 (tuần này):** `tasks/ITERATION1_[TÊN].md`
- **Iteration 2 (tuần sau):** `tasks/ITERATION2_[TÊN].md`
- **Iteration 3 (tuần cuối):** `tasks/ITERATION3_[TÊN].md`

---

## Hướng dẫn từng thành viên

Mỗi iteration có file riêng! Chỉ tập trung vào tuần hiện tại.

### Nguyễn Văn Quang Duy (Backend & Data)

**File tasks:**
- Tuần 1: `tasks/ITERATION1_QUANGDUY.md`
- Tuần 2: `tasks/ITERATION2_QUANGDUY.md`
- Tuần 3: `tasks/ITERATION3_QUANGDUY.md`

#### **Iteration 1 (27/11 - 04/12): Data Preprocessing**

**Bước 1: Setup môi trường**
```bash
# Clone project
git clone https://github.com/nguyendinhtanloc-Org/DigitalImageProcessingProject.git
cd DigitalImageProcessingProject

# Tạo branch cho mình
git checkout -b feature/data-preprocessing

# Setup môi trường Python
cd data
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Cài packages
pip install -r requirements.txt
```

**Bước 2: Download dataset**
- Đọc `data/README.md` để biết cách download
- Link: https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia
- Lưu vào thư mục: `data/raw/`

**Bước 3: Chạy preprocessing scripts**
```bash
cd data/preprocessing-scripts

# Chạy theo thứ tự:
python 01_data_inspection.py      # Kiểm tra data
python 02_data_cleaning.py        # Loại bỏ ảnh lỗi
python 03_preprocessing.py        # Resize, normalize
python 04_augmentation.py         # Data augmentation
python 05_split_dataset.py        # Chia train/val/test
```

**Bước 4: Tạo file output**
- Data đã xử lý → `data/processed/train/`, `val/`, `test/`
- Báo cáo → `data/reports/preprocessing_report.md`

**Bước 5: Commit & Push**
```bash
git add .
git commit -m "feat(data): hoàn thành preprocessing dataset"
git push origin feature/data-preprocessing
```

**Bước 6: Tạo Pull Request**
- Vào GitHub → Create PR từ `feature/data-preprocessing` → `develop`
- Tag Tấn Lộc để review

---

#### **Iteration 2 (04/12 - 11/12): Backend API**

**Bước 1: Setup Spring Boot**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/backend-api

cd backend
# Đọc backend/TASKS.md để biết chi tiết
```

**Bước 2: Tạo các file trong backend/src/main/java/com/pneumonia/**

**File cần tạo theo thứ tự:**

1. **dto/PredictionRequest.java**
   - Input: file ảnh
   - Validation: file type, size

2. **dto/PredictionResponse.java**
   - Output: prediction, confidence

3. **service/ModelClientService.java**
   - Gọi Python Flask API
   - Handle response

4. **controller/PredictionController.java**
   - Endpoint: `POST /api/predict/cnn`
   - Endpoint: `POST /api/predict/resnet50`

5. **config/SwaggerConfig.java**
   - Setup Swagger UI

**Bước 3: Test API**
```bash
# Run Spring Boot
mvn spring-boot:run

# Test với Postman
POST http://localhost:8080/api/predict/cnn
Body: form-data, key="file", value=[chọn ảnh]
```

**Bước 4: Commit**
```bash
git add .
git commit -m "feat(backend): implement prediction API endpoints"
git push origin feature/backend-api
```

---

#### **Iteration 3 (11/12 - 18/12): Optimization**

**Nhiệm vụ:**
- Fix bugs từ integration
- Optimize API performance
- Hoàn thiện Swagger docs
- Support team

**Đọc:** `backend/TASKS.md` phần Iteration 3

---

### Nguyễn Đặng Quốc Anh (Frontend & CNN)

**File tasks:**
- Tuần 1: `tasks/ITERATION1_QUOCANH.md`
- Tuần 2: `tasks/ITERATION2_QUOCANH.md`
- Tuần 3: `tasks/ITERATION3_QUOCANH.md`

#### **Iteration 1 (27/11 - 04/12): Frontend Skeleton**

**Bước 1: Setup React**
```bash
git checkout -b feature/frontend-skeleton

cd frontend
npm install
npm run dev  # Chạy dev server
```

**Bước 2: Tạo các file component trong frontend/src/**

**Cấu trúc file cần tạo:**

```
frontend/src/
├── components/
│   ├── UploadImage.jsx          ← Tạo file này trước
│   ├── ResultDisplay.jsx        ← Sau đó file này
│   └── ModelSelector.jsx        ← Cuối cùng file này
├── pages/
│   └── HomePage.jsx             ← Main page
├── services/
│   └── api.js                   ← Mock API (tạm thời)
└── App.jsx                      ← Update routing
```

**Bước 3: Implement từng component**

1. **UploadImage.jsx** - Component upload ảnh
   - Input: file upload
   - Preview ảnh
   - Validation

2. **ResultDisplay.jsx** - Hiển thị kết quả
   - Prediction: Normal/Pneumonia
   - Confidence: 95.2%
   - Dùng **mock data** tạm

3. **ModelSelector.jsx** - Chọn model
   - Radio button: CNN / ResNet50

**Bước 4: Test với mock data**
```javascript
// services/api.js (mock)
export const predictImage = async (file, model) => {
  // Fake API response
  return {
    prediction: "Pneumonia",
    confidence: 95.2
  };
};
```

**Bước 5: Commit**
```bash
git add .
git commit -m "feat(frontend): create basic UI components"
git push origin feature/frontend-skeleton
```

---

#### **Iteration 2 (04/12 - 11/12): CNN Training**

**Bước 1: Lên Kaggle**
- Upload file `notebooks/CNN.ipynb` lên Kaggle
- Add dataset: Chest X-Ray Pneumonia
- Enable GPU: T4 x2

**Bước 2: Train model**
- Chỉnh code trong notebook
- Train ~2-3 giờ
- Save model: `cnn_best.h5`

**Bước 3: Download model**
- Download `cnn_best.h5` từ Kaggle
- Lưu vào `models/cnn_best.h5` trong project

**Bước 4: Tạo React components thật**
```bash
git checkout -b feature/react-components

cd frontend/src/components
# Update UploadImage, ResultDisplay với design đẹp hơn
```

**Bước 5: Commit**
```bash
git add .
git commit -m "feat(ml): train CNN model, accuracy 92%"
git add models/cnn_best.h5
git commit -m "feat(ml): add trained CNN model"
git push origin feature/react-components
```

---

#### **Iteration 3 (11/12 - 18/12): Frontend-Backend Connect**

**Bước 1: Update API service**
```javascript
// frontend/src/services/api.js
import axios from 'axios';

const API_BASE = 'http://localhost:8080/api';

export const predictImage = async (file, modelType) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const endpoint = modelType === 'cnn' 
    ? `${API_BASE}/predict/cnn`
    : `${API_BASE}/predict/resnet50`;
    
  const response = await axios.post(endpoint, formData);
  return response.data;
};
```

**Bước 2: Update components dùng real API**

**Bước 3: Polish UI**
- Responsive design
- Loading states
- Error handling

---

### Nguyễn Đình Tấn Lộc (ResNet50 & Integration)

**File tasks:**
- Tuần 1: `tasks/ITERATION1_TANLOC.md`
- Tuần 2: `tasks/ITERATION2_TANLOC.md`
- Tuần 3: `tasks/ITERATION3_TANLOC.md`

#### **Iteration 1 (27/11 - 04/12): Preview Logic**

**Bước 1: Setup**
```bash
git checkout -b feature/preview-logic

cd frontend/src/components
```

**Bước 2: Tạo file ImagePreview.jsx**
```javascript
// ImagePreview.jsx
import { useState } from 'react';

export default function ImagePreview({ file }) {
  const [preview, setPreview] = useState(null);
  
  useEffect(() => {
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => setPreview(reader.result);
      reader.readAsDataURL(file);
    }
  }, [file]);
  
  return preview ? <img src={preview} alt="Preview" /> : null;
}
```

**Bước 3: Commit**
```bash
git add .
git commit -m "feat(frontend): add image preview logic"
git push origin feature/preview-logic
```

---

#### **Iteration 2 (04/12 - 11/12): ResNet50 Training**

**Bước 1: Lên Kaggle**
- Upload `notebooks/ResNet.ipynb`
- Add dataset
- Enable GPU

**Bước 2: Fine-tune ResNet50**
```python
# Trong notebook
from tensorflow.keras.applications import ResNet50

base_model = ResNet50(weights='imagenet', include_top=False)
# ... fine-tune code
```

**Bước 3: Download model**
- Save: `resnet50_best.h5`
- Lưu vào `models/resnet50_best.h5`

**Bước 4: Setup Flask (optional)**
```bash
cd model-service
pip install -r requirements.txt
python app/main.py  # Test Flask API
```

---

#### **Iteration 3 (11/12 - 18/12): Integration**

**Bước 1: Frontend-Backend Integration**
```bash
git checkout -b feature/integration

# Test full flow:
Frontend → Backend → Model Service → Response
```

**Bước 2: Tạo file integration test**
```bash
# Test từng bước:
1. Upload ảnh từ frontend
2. Check backend nhận được
3. Check model service trả kết quả
4. Check frontend hiển thị đúng
```

**Bước 3: Model Comparison**
```bash
cd notebooks/comparison
# Tạo notebook so sánh CNN vs ResNet50
jupyter notebook Model_Comparison.ipynb
```

**Bước 4: Viết báo cáo**
- File: `docs/model_comparison_report.md`
- Nội dung: Accuracy, Loss curves, Confusion Matrix

**Bước 5: Docker Deployment**
```bash
cd deployment
docker-compose up --build

# Test toàn bộ hệ thống
curl http://localhost:3000  # Frontend
curl http://localhost:8080  # Backend
curl http://localhost:5000  # Model Service
```

---

## Checklist từng tuần

### Week 1 (27/11 - 04/12)

- [ ] **Quang Duy:** Dataset preprocessing xong
- [ ] **Quốc Anh:** Frontend UI skeleton xong
- [ ] **Tấn Lộc:** Preview logic xong
- [ ] **Meeting 04/12:** Demo progress, plan tuần sau

### Week 2 (04/12 - 11/12)

- [ ] **Quang Duy:** Spring Boot API xong
- [ ] **Quốc Anh:** CNN model trained + React components
- [ ] **Tấn Lộc:** ResNet50 model trained
- [ ] **Meeting 11/12:** Demo API + Models

### Week 3 (11/12 - 18/12)

- [ ] **Quốc Anh:** Frontend connect API
- [ ] **Tấn Lộc:** Full integration + comparison report
- [ ] **Quang Duy:** API optimization
- [ ] **Meeting 18/12:** Final demo

---

## Quy trình hàng ngày

### 1. Trước khi code

```bash
# Pull code mới nhất
git checkout develop
git pull origin develop

# Tạo branch mới (hoặc checkout branch cũ)
git checkout -b feature/ten-feature
```

### 2. Trong khi code

```bash
# Commit thường xuyên (mỗi 1-2 tiếng)
git add .
git commit -m "feat: mô tả ngắn gọn"
```

### 3. Sau khi xong task

```bash
# Push code
git push origin feature/ten-feature

# Tạo Pull Request trên GitHub
# Tag người review
```

### 4. Khi có người review

- Đọc comments
- Sửa code theo góp ý
- Push lại
- Merge vào develop

---

## Lưu ý quan trọng

### Không commit những file này:
- `data/raw/*` - Dataset gốc (quá lớn)
- `data/processed/*` - Dataset đã xử lý (quá lớn)
- `models/*.h5` - Models (quá lớn, dùng Git LFS hoặc Google Drive)
- `node_modules/` - Node.js dependencies
- `venv/`, `env/` - Python virtual environment
- `.env` - Environment variables
- `__pycache__/` - Python cache

### Luôn pull trước khi push:
```bash
git pull origin develop --rebase
```

### Nếu conflict:
```bash
# Sửa file conflict
git add .
git rebase --continue
```

---

## File quan trọng phải đọc

1. **README.md** - Tổng quan dự án
2. **TIMELINE.md** - Timeline chi tiết 3 tuần
3. **CONTRIBUTING.md** - Quy tắc commit, branch
4. **Task file của bạn** - Chi tiết công việc

---

## Câu hỏi thường gặp

**Q: Tôi không biết bắt đầu từ đâu?**
A: Đọc file này từ đầu → README.md → TIMELINE.md → Task file của bạn

**Q: Tôi nên tạo branch như thế nào?**
A: `git checkout -b feature/ten-feature` (đọc CONTRIBUTING.md)

**Q: Commit message viết sao?**
A: `feat(scope): mô tả` (đọc CONTRIBUTING.md)

**Q: File nào không được commit?**
A: Xem `.gitignore` và phần "Lưu ý quan trọng" ở trên

**Q: Làm sao biết task mình xong chưa?**
A: Tick checkbox trong TIMELINE.md hoặc task file của bạn

**Q: Khi nào cần review code?**
A: Mỗi khi tạo Pull Request (trước khi merge vào develop)

---

## Liên hệ hỗ trợ

- **Quang Duy:** Backend, Data issues
- **Quốc Anh:** Frontend, CNN issues
- **Tấn Lộc:** Integration, ResNet50 issues

**Group chat:** [Link Discord/Zalo]

---

**Chúc các bạn code vui!**

*Cập nhật lần cuối: 27/11/2025*
