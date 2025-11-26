# Hướng dẫn đóng góp cho dự án

Cảm ơn bạn đã quan tâm đến dự án! Tài liệu này sẽ hướng dẫn cách làm việc hiệu quả với team.

##  Mục lục

- [Git Workflow](#git-workflow)
- [Branching Strategy](#branching-strategy)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Code Style](#code-style)
- [Code Review](#code-review)

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
