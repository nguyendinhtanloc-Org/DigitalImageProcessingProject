# Backend - Spring Boot API

## Mô tả

Backend API cho dự án Pneumonia Detection, xây dựng bằng **Spring Boot 3.x**, cung cấp RESTful API để xử lý upload ảnh X-ray và dự đoán kết quả.

## Công nghệ

- **Java 17+**
- **Spring Boot 3.x**
- **Spring Web** - REST API
- **Maven** - Build tool
- **Springdoc OpenAPI** - API Documentation (Swagger)
- **Lombok** - Reduce boilerplate code

## Cấu trúc

```
backend/
├── src/
│   ├── main/
│   │   ├── java/com/pneumonia/
│   │   │   ├── controller/          # REST Controllers
│   │   │   │   ├── PredictionController.java
│   │   │   │   └── HealthController.java
│   │   │   ├── service/             # Business Logic
│   │   │   │   ├── PredictionService.java
│   │   │   │   └── ImageProcessingService.java
│   │   │   ├── dto/                 # Data Transfer Objects
│   │   │   │   ├── PredictionRequest.java
│   │   │   │   └── PredictionResponse.java
│   │   │   ├── config/              # Configuration
│   │   │   │   ├── CorsConfig.java
│   │   │   │   └── SwaggerConfig.java
│   │   │   └── PneumoniaDetectionApplication.java
│   │   └── resources/
│   │       ├── application.properties
│   │       └── application-dev.properties
│   └── test/
│       └── java/com/pneumonia/
│           └── controller/
│               └── PredictionControllerTest.java
├── pom.xml
└── README.md
```

## Setup và Chạy

### Prerequisites

- Java 17 hoặc cao hơn
- Maven 3.8+

### 1. Cài đặt dependencies

```bash
cd backend
mvn clean install
```

### 2. Chạy application

**Development mode:**
```bash
mvn spring-boot:run
```

**Hoặc build và chạy jar:**
```bash
mvn clean package
java -jar target/pneumonia-detection-backend-1.0.0.jar
```

### 3. Verify

Server chạy tại: `http://localhost:8080`

**Health check:**
```bash
curl http://localhost:8080/api/health
```

**Swagger UI:**
```
http://localhost:8080/swagger-ui.html
```

## API Endpoints

### 1. Predict Pneumonia

**POST** `/api/predict`

Upload ảnh X-ray và nhận kết quả dự đoán.

**Request:**
```bash
curl -X POST http://localhost:8080/api/predict \
  -F "file=@/path/to/xray-image.jpg" \
  -F "model=cnn"  # hoặc "resnet50"
```

**Response:**
```json
{
  "prediction": "PNEUMONIA",
  "confidence": 0.9542,
  "model": "cnn",
  "timestamp": "2024-11-27T10:30:45Z"
}
```

### 2. Grad-CAM Visualization

**POST** `/api/gradcam`

Upload ảnh và nhận heatmap Grad-CAM.

**Request:**
```bash
curl -X POST http://localhost:8080/api/gradcam \
  -F "file=@/path/to/xray-image.jpg" \
  -F "model=resnet50"
```

**Response:**
```json
{
  "prediction": "PNEUMONIA",
  "confidence": 0.9542,
  "heatmap": "data:image/png;base64,iVBORw0KGgoAAAANS..."
}
```

### 3. Health Check

**GET** `/api/health`

Kiểm tra trạng thái server.

**Response:**
```json
{
  "status": "UP",
  "timestamp": "2024-11-27T10:30:45Z"
}
```

## Configuration

### application.properties

```properties
# Server
server.port=8080

# File Upload
spring.servlet.multipart.max-file-size=10MB
spring.servlet.multipart.max-request-size=10MB

# Python Model Service
python.model.url=http://localhost:5000
python.model.timeout=30000

# CORS
cors.allowed-origins=http://localhost:5173
```

### Environment Variables

Tạo file `.env` (không commit vào Git):

```bash
PYTHON_MODEL_URL=http://localhost:5000
UPLOAD_DIR=/tmp/uploads
```

## Testing

### Chạy unit tests

```bash
mvn test
```

### Chạy integration tests

```bash
mvn verify
```

### Test coverage

```bash
mvn clean test jacoco:report
# Xem report tại: target/site/jacoco/index.html
```

## Build cho Production

```bash
# Build jar file
mvn clean package -DskipTests

# Jar file sẽ được tạo tại:
# target/pneumonia-detection-backend-1.0.0.jar
```

## Docker

**Dockerfile:**
```dockerfile
FROM openjdk:17-jdk-slim
WORKDIR /app
COPY target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

**Build và chạy:**
```bash
docker build -t pneumonia-backend .
docker run -p 8080:8080 pneumonia-backend
```

## Development

### Code Style

- Tuân theo **Google Java Style Guide**
- Sử dụng **Lombok** để giảm boilerplate
- Sử dụng **Constructor Injection** thay vì Field Injection

### Logging

```java
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Service
public class PredictionService {
    public PredictionResponse predict(MultipartFile file) {
        log.info("Processing prediction for file: {}", file.getOriginalFilename());
        // ...
    }
}
```

## Troubleshooting

### Lỗi CORS

Kiểm tra `CorsConfig.java` và `cors.allowed-origins` trong config.

### Lỗi File Upload quá lớn

Tăng giá trị trong `application.properties`:
```properties
spring.servlet.multipart.max-file-size=20MB
spring.servlet.multipart.max-request-size=20MB
```

### Python Model không kết nối được

Kiểm tra:
1. Python service đang chạy tại đúng port
2. URL trong config đúng
3. Network/firewall không block

## Resources

- [Spring Boot Documentation](https://spring.io/projects/spring-boot)
- [Springdoc OpenAPI](https://springdoc.org/)
- [Maven Central](https://search.maven.org/)

---

**Liên hệ:** Backend Team - backend@example.com
