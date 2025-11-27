# Hướng dẫn đóng góp cho dự án

Cảm ơn bạn đã quan tâm đến dự án Pneumonia Detection! Tài liệu này sẽ hướng dẫn cách làm việc hiệu quả với team.

## Mục lục

- [Git Workflow](#git-workflow)
- [Branching Strategy](#branching-strategy)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Code Style](#code-style)
- [Development Setup](#development-setup)

---

## Git Workflow

### Bước 1: Clone Repository

```bash
# Clone repository
git clone https://github.com/nguyendinhtanloc-Org/DigitalImageProcessingProject.git
cd DigitalImageProcessingProject
```

### Bước 2: Đồng bộ code mới nhất

```bash
# Chuyển về develop
git checkout develop

# Lấy code mới nhất
git pull origin develop
```

### Bước 3: Tạo branch mới cho tính năng

```bash
# Tạo branch từ develop
git checkout -b feature/ten-tinh-nang

# Hoặc cho bugfix
git checkout -b fix/ten-bug
```

### Bước 4: Commit code

```bash
# Thêm files đã thay đổi
git add .

# Commit với message rõ ràng (KHÔNG dùng emojis/icons)
git commit -m "Add Grad-CAM visualization for model interpretability"
```

### Bước 5: Push và tạo Pull Request

```bash
# Push lên origin
git push origin feature/ten-tinh-nang

# Sau đó tạo Pull Request trên GitHub
```

---

## Branching Strategy

Dự án sử dụng **Git Flow** đơn giản với các loại branch sau:

### Branch chính

- **`main`**: Code production, stable
  - Chỉ merge từ `develop` khi release
  - Không commit trực tiếp vào branch này

- **`develop`**: Branch development chính
  - Tất cả features được merge vào đây
  - Code luôn ở trạng thái có thể chạy được

### Branch phụ

- **`feature/*`**: Phát triển tính năng mới
  - Format: `feature/ten-tinh-nang`
  - Ví dụ: `feature/image-enhancement`, `feature/model-performance-dashboard`
  - Tạo từ: `develop`
  - Merge vào: `develop`

- **`fix/*`**: Sửa bug
  - Format: `fix/ten-bug`
  - Ví dụ: `fix/css-gradient-safari`, `fix/file-upload-validation`
  - Tạo từ: `develop`
  - Merge vào: `develop`

- **`ui/*`**: Cải thiện UI/UX
  - Format: `ui/component-name`
  - Ví dụ: `ui/prediction-card-redesign`

- **`docs/*`**: Cập nhật documentation
  - Format: `docs/section-name`
  - Ví dụ: `docs/readme-update`

### Quy tắc đặt tên branch

**Đúng:**
```
feature/gradcam-heatmap
fix/macos-crash-issue
ui/modern-prediction-cards
docs/setup-guide
```

**Sai:**
```
upload-image           # Thiếu prefix
feature/Upload_Image   # Sử dụng underscore và viết hoa
fix-bug                # Không rõ ràng
my-branch              # Không theo convention
```

---

## Commit Guidelines

### Format commit message

**QUAN TRỌNG: KHÔNG sử dụng emojis/icons trong commit messages**

Format: **`<subject>`** hoặc **`<type>: <subject>`**

```
Add HCMUTE logo and university branding to header
Fix macOS TensorFlow crash with mutex lock error
Update UI with modern gradient design
Refactor prediction card component for better performance
```

### Các Type commit (optional)

| Type | Mô tả | Ví dụ |
|------|-------|-------|
| `Add` | Thêm tính năng mới | `Add Grad-CAM visualization page` |
| `Fix` | Sửa bug | `Fix CORS error on file upload` |
| `Update` | Cập nhật code/docs | `Update README with setup instructions` |
| `Refactor` | Refactor code | `Refactor CSS with variables` |
| `Remove` | Xóa code/file | `Remove unused emojis from UI` |
| `Improve` | Cải thiện performance/UX | `Improve prediction card animations` |

### Subject (Mô tả)

- Viết **chữ thường đầu câu**, không dấu chấm cuối
- Sử dụng **thì hiện tại**: "Add" thay vì "Added"
- Tối đa **72 ký tự**
- Mô tả **rõ ràng** những gì đã làm
- **KHÔNG dùng emojis** (🚀, ✨, 🎨, etc.)

### Ví dụ commit message tốt

```bash
Add model performance comparison dashboard
Fix TensorFlow import error on macOS
Update styles.css with modern gradient theme
Refactor ui_components for cleaner code
Remove all emojis from application
Improve responsive design for mobile devices
Add HCMUTE university branding to footer
```

### Commit message có body (nếu cần)

```bash
git commit -m "Add Grad-CAM visualization feature

- Create new page for Grad-CAM heatmaps
- Implement overlay function for original image
- Add interpretation guide section
- Update navigation menu

Closes #45"
```

---

## Pull Request Process

### 1. Chuẩn bị Pull Request

**Trước khi tạo PR:**
- Code đã chạy thành công local
- Đã test trên browser (Chrome, Safari)
- Code đã format đúng style
- Đã commit với message rõ ràng
- Branch đã sync với `develop` mới nhất
- **KHÔNG có emojis trong code**

```bash
# Sync với develop
git checkout develop
git pull origin develop
git checkout feature/your-feature
git merge develop

# Giải quyết conflicts nếu có
# Sau đó push
git push origin feature/your-feature
```

### 2. Tạo Pull Request

**Title (KHÔNG dùng emojis):**
```
Add image enhancement tools with CLAHE and denoising
```

**Description template:**

```markdown
## Mô tả

Thêm trang Image Enhancement với các công cụ tiền xử lý ảnh X-ray.

## Thay đổi

- Tạo page `3_Image_Enhancement.py`
- Thêm brightness/contrast sliders
- Implement CLAHE algorithm
- Add denoising với adjustable strength
- Download button cho enhanced images

## Checklist

- [x] Code chạy thành công local
- [x] Đã test trên Chrome và Safari
- [x] Đã format code theo PEP 8
- [x] Không có emojis/icons trong code
- [x] CSS responsive cho mobile
- [ ] Cần review performance optimization

## Related Issues

Closes #23

## Screenshots

![Enhancement Tools](link-to-screenshot)
```

### 3. Review Process

**Người tạo PR:**
- Tự review code trước khi request review
- Trả lời comments rõ ràng
- Update code theo feedback
- Resolve conversations khi đã fix

**Reviewer:**
- Review trong vòng **24 giờ**
- Comment **constructive feedback**
- Approve nếu code đạt yêu cầu
- Request changes nếu cần sửa

### 4. Merge Pull Request

**Điều kiện để merge:**
- Có ít nhất **1 approval** từ team member
- Code đã được test kỹ
- Không có **merge conflicts**
- Không có emojis/icons trong code

**Merge strategy:**
- Sử dụng **"Squash and merge"** để giữ history sạch
- Delete branch sau khi merge

---

## Code Style

### Python (Streamlit App)

**Style guide:** PEP 8

```python
# Đúng
import streamlit as st
from PIL import Image
import numpy as np

def render_prediction_card(prediction, confidence, model_name):
    """
    Render prediction result card with modern design
    
    Args:
        prediction (str): "Normal" or "Pneumonia"
        confidence (float): Confidence score (0-100)
        model_name (str): Name of the model used
    """
    css_class = "normal" if prediction.upper() == "NORMAL" else "pneumonia"
    
    st.markdown(f"""
    <div class="prediction-card {css_class}">
        <div class="prediction-label">{prediction.upper()}</div>
        <div class="confidence-badge">{confidence:.1f}% Confidence</div>
    </div>
    """, unsafe_allow_html=True)

# Sai
def RenderCard(pred,conf):  # Naming không đúng
    st.markdown(f"<div>🎉 {pred}</div>")  # Có emoji
```

**Convention:**
- Function names: `snake_case`
- Class names: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Variables: `snake_case`
- **KHÔNG dùng emojis** trong code
- Docstrings cho tất cả functions
- Maximum line length: 88 characters (Black formatter)

### CSS

```css
/* Đúng */
:root {
    --primary-color: #0066CC;
    --success-color: #00C853;
    --border-radius: 12px;
}

.prediction-card {
    background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
    border-radius: var(--border-radius);
    padding: 1.5rem;
    transition: all 0.3s ease;
}

/* Sai */
.card {
    background: #fff;  /* Nên dùng CSS variables */
    padding: 20px;     /* Nên dùng rem */
}
```

**Convention:**
- Sử dụng CSS variables cho colors
- Spacing với `rem` thay vì `px`
- Class names: `kebab-case`
- Group related properties
- Comment cho các sections phức tạp

### Markdown

**Đúng:**
```markdown
## Setup Instructions

### Requirements
- Python 3.12+
- pip packages listed in requirements.txt

### Installation
1. Create virtual environment
2. Install dependencies
3. Run application
```

**Sai:**
```markdown
## 🚀 Setup Instructions

### ✅ Requirements
- Python 3.12+ ⚡
- pip packages 📦
```

**KHÔNG dùng emojis** trong:
- Headings
- List items
- File names
- Code comments

---

## Development Setup

### Yêu cầu

- Python 3.12 hoặc cao hơn
- pip (Python package manager)
- Git

### Setup môi trường

```bash
# Di chuyển vào thư mục app
cd app

# Tạo virtual environment
python3.12 -m venv venv

# Kích hoạt venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Cài dependencies
pip install -r requirements.txt
```

### Chạy app local

**macOS (Khuyến nghị):**
```bash
./run.sh
```

**Manual:**
```bash
# macOS
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
streamlit run app.py

# Windows/Linux
streamlit run app.py
```

App sẽ chạy tại: **http://localhost:8501**

### Testing

```bash
# Test trên browser
open http://localhost:8501

# Test upload file
# Test model selection
# Test responsive design (DevTools > Toggle device toolbar)
```

---

## Lưu ý quan trọng

### DO

- **Commit thường xuyên** với messages rõ ràng
- **Test kỹ** trước khi push
- **Sync với develop** thường xuyên
- **Review code** của người khác
- **Ask questions** nếu không rõ
- **Format code** với Black (Python)
- **Kiểm tra responsive** design

### DON'T

- **KHÔNG dùng emojis/icons** trong code, commits, hoặc PRs
- **Không commit** code không chạy được
- **Không push** trực tiếp vào `main` hoặc `develop`
- **Không merge** PR của chính mình
- **Không commit** files không cần thiết (venv/, __pycache__/, .DS_Store)
- **Không hardcode** credentials hoặc API keys

---

## Project Structure

```
DigitalImageProcessingProject/
├── app/                          # Streamlit application
│   ├── app.py                    # Main page
│   ├── pages/                    # Multi-page app
│   │   ├── 1_Model_Performance.py
│   │   ├── 2_Grad-CAM_Visualization.py
│   │   └── 3_Image_Enhancement.py
│   ├── utils/                    # Helper functions
│   │   ├── ui_components.py
│   │   ├── visualization.py
│   │   └── image_processing.py
│   ├── static/                   # CSS, images
│   │   └── styles.css
│   └── requirements.txt
├── models/                       # Trained models (gitignored)
├── notebooks/                    # Jupyter notebooks for training
└── README.md
```

---

## Resources

- [PEP 8 - Python Style Guide](https://peps.python.org/pep-0008/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Git Flow Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
- [Black Code Formatter](https://black.readthedocs.io/)

---

## Team

**Team Prompt Engineer**
- Trường Đại học Sư phạm Kỹ thuật TP. Hồ Chí Minh (HCMUTE)
- Môn học: Xử Lý Ảnh Số
- Giảng viên: ThS. Đoàn Minh Trí

---

**Happy Coding!**


---

## Git Workflow

### Bước 1: Fork và Clone (lần đầu tiên)

```bash
# Clone repository
git clone https://github.com/nguyendinhtanloc-Org/DigitalImageProcessingProject.git
cd DigitalImageProcessingProject

# Thêm remote upstream để đồng bộ với repo gốc
git remote add upstream https://github.com/nguyendinhtanloc-Org/DigitalImageProcessingProject.git
```

### Bước 2: Đồng bộ code mới nhất

```bash
# Chuyển về develop
git checkout develop

# Lấy code mới nhất từ upstream
git fetch upstream
git merge upstream/develop

# Hoặc sử dụng pull
git pull upstream develop

# Push về origin của bạn
git push origin develop
```

### Bước 3: Tạo branch mới cho tính năng

```bash
# Tạo branch từ develop
git checkout -b feature/ten-tinh-nang

# Hoặc cho bugfix
git checkout -b fix/ten-bug
```

### Bước 4: Commit code

```bash
# Thêm files đã thay đổi
git add .

# Commit với message rõ ràng
git commit -m "feat(backend): thêm API upload ảnh X-ray"
```

### Bước 5: Push và tạo Pull Request

```bash
# Push lên origin
git push origin feature/ten-tinh-nang

# Sau đó tạo Pull Request trên GitHub
```

---

## Branching Strategy

Dự án sử dụng **Git Flow** với các loại branch sau:

### Branch chính

- **`main`**: Code production, stable, đã test kỹ
  - Chỉ merge từ `develop` khi release
  - Không commit trực tiếp vào branch này

- **`develop`**: Branch development chính
  - Tất cả features được merge vào đây
  - Code luôn ở trạng thái có thể build

### Branch phụ

- **`feature/*`**: Phát triển tính năng mới
  - Format: `feature/ten-tinh-nang`
  - Ví dụ: `feature/upload-image`, `feature/gradcam-visualization`
  - Tạo từ: `develop`
  - Merge vào: `develop`

- **`fix/*`**: Sửa bug
  - Format: `fix/ten-bug`
  - Ví dụ: `fix/cors-error`, `fix/image-resize`
  - Tạo từ: `develop`
  - Merge vào: `develop`

- **`hotfix/*`**: Sửa bug khẩn cấp trên production
  - Format: `hotfix/critical-bug`
  - Tạo từ: `main`
  - Merge vào: `main` và `develop`

- **`refactor/*`**: Refactor code
  - Format: `refactor/module-name`
  - Ví dụ: `refactor/api-service`

### Quy tắc đặt tên branch

 **Đúng:**
```
feature/upload-xray-image
fix/login-validation-error
refactor/cnn-model-architecture
hotfix/critical-api-crash
```

 **Sai:**
```
upload-image           # Thiếu prefix
feature/Upload_Image   # Sử dụng underscore và viết hoa
fix-bug                # Không rõ ràng
my-branch              # Không theo convention
```

---

## Commit Guidelines

### Conventional Commits

Tuân theo format: **`<type>(<scope>): <subject>`**

```
feat(backend): thêm API upload ảnh X-ray
│    │         │
│    │         └─> Mô tả ngắn gọn (lowercase)
│    │
│    └─────────> Phạm vi (optional): backend, frontend, models, docs
│
└──────────────> Type: feat, fix, docs, style, refactor, test, chore
```

### Các Type commit

| Type | Mô tả | Ví dụ |
|------|-------|-------|
| `feat` | Tính năng mới | `feat(frontend): thêm component hiển thị kết quả` |
| `fix` | Sửa bug | `fix(backend): sửa lỗi CORS khi call API` |
| `docs` | Cập nhật tài liệu | `docs: cập nhật hướng dẫn setup trong README` |
| `style` | Format code, không thay đổi logic | `style(frontend): format code theo Prettier` |
| `refactor` | Refactor code | `refactor(models): tối ưu data preprocessing` |
| `test` | Thêm hoặc sửa tests | `test(backend): thêm unit test cho PredictService` |
| `chore` | Cập nhật dependencies, config | `chore: cập nhật Spring Boot lên 3.2.0` |
| `perf` | Cải thiện performance | `perf(models): tối ưu tốc độ inference` |

### Scope (Phạm vi)

- `backend`: Spring Boot API
- `frontend`: ReactJS application
- `models`: AI/ML models (CNN, ResNet)
- `docs`: Documentation
- `data`: Dataset, preprocessing

### Subject (Mô tả)

- Viết **chữ thường**, không dấu chấm cuối
- Sử dụng **thì hiện tại**: "thêm" thay vì "đã thêm"
- Tối đa **50 ký tự**
- Mô tả **rõ ràng** những gì đã làm

### Ví dụ commit message tốt

```bash
feat(backend): thêm endpoint POST /api/predict cho dự đoán ảnh
fix(frontend): sửa lỗi hiển thị confidence score
docs: thêm hướng dẫn train model trong README
style(models): format Python code theo PEP 8
refactor(backend): tách service layer khỏi controller
test(frontend): thêm unit test cho UploadComponent
chore: cập nhật dependencies trong pom.xml
perf(models): giảm thời gian inference từ 2s xuống 0.5s
```

### Commit message có body (nếu cần)

```bash
git commit -m "feat(backend): thêm Grad-CAM API endpoint

- Tạo service xử lý Grad-CAM
- Thêm endpoint POST /api/gradcam
- Tích hợp với Python model
- Trả về heatmap dạng base64

Closes #123"
```

---

## Pull Request Process

### 1. Chuẩn bị Pull Request

**Trước khi tạo PR:**
-  Code đã build thành công
-  Đã test local và không có lỗi
-  Code đã format đúng style
-  Đã commit với message rõ ràng
-  Branch đã sync với `develop` mới nhất

```bash
# Sync với develop
git checkout develop
git pull upstream develop
git checkout feature/your-feature
git merge develop

# Giải quyết conflicts nếu có
# Sau đó push
git push origin feature/your-feature
```

### 2. Tạo Pull Request

**Title:**
```
feat(backend): thêm API upload và dự đoán ảnh X-ray
```

**Description template:**

```markdown
## 📋 Mô tả

Thêm chức năng upload ảnh X-ray và gọi model để dự đoán kết quả.

## 🔧 Thay đổi

- Tạo `ImageController` với endpoint `/api/upload`
- Thêm `PredictionService` để gọi Python model
- Xử lý file upload với MultipartFile
- Trả về JSON response với prediction và confidence

##  Checklist

- [x] Code build thành công
- [x] Đã test local
- [x] Đã format code
- [x] Đã cập nhật documentation (nếu cần)
- [ ] Cần review kỹ phần error handling

## 🔗 Related Issues

Closes #45

## 📸 Screenshots (nếu có)

![API Response](link-to-image)
```

### 3. Review Process

**Người tạo PR:**
- Tự review code trước khi request review
- Trả lời comments một cách rõ ràng
- Update code theo feedback
- Resolve conversations khi đã fix

**Reviewer:**
- Review trong vòng **24 giờ**
- Comment **constructive feedback**
- Approve nếu code đạt yêu cầu
- Request changes nếu cần sửa

### 4. Merge Pull Request

**Điều kiện để merge:**
-  Có ít nhất **1 approval** từ team member
-  Tất cả **CI/CD checks pass**
-  Không có **merge conflicts**
-  Code đã được review kỹ

**Merge strategy:**
- Sử dụng **"Squash and merge"** để giữ history sạch
- Delete branch sau khi merge

---

## Code Style

### Backend (Java/Spring Boot)

**Style guide:** Google Java Style Guide

```java
//  Đúng
@RestController
@RequestMapping("/api/predictions")
public class PredictionController {
    
    private final PredictionService predictionService;
    
    @PostMapping("/upload")
    public ResponseEntity<PredictionResponse> predict(
            @RequestParam("file") MultipartFile file) {
        // Implementation
    }
}

//  Sai
@RestController
public class predictionController {  // Tên class phải viết hoa
    @Autowired
    PredictionService service;  // Nên dùng constructor injection
}
```

**Convention:**
- Class names: `PascalCase`
- Methods/variables: `camelCase`
- Constants: `UPPER_SNAKE_CASE`
- Sử dụng constructor injection thay vì field injection
- Comments bằng tiếng Anh

### Frontend (ReactJS)

**Style guide:** Airbnb JavaScript Style Guide

```jsx
//  Đúng
import React, { useState } from 'react';

const UploadImage = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  
  const handleUpload = async () => {
    // Implementation
  };
  
  return (
    <div className="container">
      {/* JSX */}
    </div>
  );
};

export default UploadImage;

//  Sai
function uploadImage() {  // Component name phải viết hoa
  var file;  // Dùng const/let thay vì var
  
  return <div>...</div>
}
```

**Convention:**
- Component names: `PascalCase`
- Functions/variables: `camelCase`
- Files: `PascalCase.jsx` cho components
- Sử dụng functional components + hooks
- TailwindCSS cho styling

### AI/ML (Python)

**Style guide:** PEP 8

```python
#  Đúng
import tensorflow as tf
from tensorflow import keras

class CNNModel:
    """Custom CNN model for pneumonia detection."""
    
    def __init__(self, input_shape=(224, 224, 3)):
        self.input_shape = input_shape
        self.model = self._build_model()
    
    def _build_model(self):
        """Build CNN architecture."""
        model = keras.Sequential([
            # Layers
        ])
        return model

#  Sai
import tensorflow as tf

class cnnModel:  # Class name phải PascalCase
    def __init__(self,input_shape):  # Thiếu space sau dấu phẩy
        self.Model=self.BuildModel()  # Không theo naming convention
```

**Convention:**
- Class names: `PascalCase`
- Functions/variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Docstrings cho tất cả functions/classes
- Maximum line length: 88 (Black formatter)

### Format code tự động

**Python:**
```bash
# Install Black
pip install black

# Format
black models/
```

**JavaScript:**
```bash
# Install Prettier
npm install --save-dev prettier

# Format
npm run format
```

---

## Code Review

### Review checklist

**Functionality:**
- [ ] Code có hoạt động đúng như mong đợi?
- [ ] Edge cases đã được xử lý?
- [ ] Error handling có đầy đủ?

**Code Quality:**
- [ ] Code dễ đọc và maintain?
- [ ] Có duplicate code không?
- [ ] Naming rõ ràng và có ý nghĩa?
- [ ] Comments có cần thiết không?

**Performance:**
- [ ] Có vấn đề về performance?
- [ ] Database queries có tối ưu?
- [ ] Memory leaks?

**Security:**
- [ ] Input validation đầy đủ?
- [ ] Sensitive data được bảo mật?
- [ ] SQL injection, XSS được prevent?

**Testing:**
- [ ] Có unit tests?
- [ ] Tests có cover được cases quan trọng?

### Comment examples

**Request changes:**
```
Cần sửa: Method này nên validate input trước khi xử lý

Suggestion:
if (file == null || file.isEmpty()) {
    throw new IllegalArgumentException("File cannot be empty");
}
```

**Suggestion:**
```
Gợi ý: Nên tách logic này thành một service riêng để dễ test và reuse
```

**Praise:**
```
Tốt: Error handling rất tốt, đã cover được nhiều cases
```

**Question:**
```
Câu hỏi: Tại sao ở đây dùng ArrayList thay vì HashSet?
```

---

## Lưu ý quan trọng

### DO

- **Commit thường xuyên** với messages rõ ràng
- **Test kỹ** trước khi push
- **Sync với develop** thường xuyên để tránh conflicts
- **Review kỹ** code của người khác
- **Ask questions** nếu không rõ

### DON'T

- **Không commit** code không chạy được
- **Không push** trực tiếp vào `main` hoặc `develop`
- **Không merge** PR của chính mình (trừ hotfix khẩn cấp)
- **Không commit** files không cần thiết (node_modules, .env, ...)
- **Không force push** nếu không thực sự cần thiết

---

## Resources

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html)
- [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- [PEP 8 - Python Style Guide](https://peps.python.org/pep-0008/)
- [Git Flow Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)

---

## Liên hệ

Nếu có câu hỏi, liên hệ qua:
- Team chat: [Discord/Slack link]
- Email: team@example.com

---

**Happy Coding!**
