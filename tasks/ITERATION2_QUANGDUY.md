# Iteration 2 - Quang Duy (04/12 - 11/12)

**Mục tiêu:** Spring Boot API hoàn chỉnh

---

## Checklist

### Ngày 1-2 (04-05/12): Project Setup

- [ ] Init Spring Boot project
  - Spring Web
  - Spring Boot DevTools
  - Lombok
  - Springdoc OpenAPI (Swagger)

- [ ] Tạo package structure:
  ```
  com.pneumonia/
  ├── controller/
  ├── service/
  ├── dto/
  ├── config/
  └── exception/
  ```

- [ ] Config `application.properties`:
  - Server port: 8080
  - CORS settings
  - File upload max size: 10MB
  - Model service URL: http://localhost:5000

### Ngày 3-4 (06-07/12): Core API Development

- [ ] Tạo DTOs:
  - `PredictionRequest.java`
  - `PredictionResponse.java`

- [ ] Tạo `ModelClientService.java`:
  - Call Python Flask API
  - Handle HTTP requests
  - Parse JSON response

- [ ] Tạo `PredictionController.java`:
  - `POST /api/predict/cnn`
  - `POST /api/predict/resnet50`
  - Validate file upload
  - Return JSON response

### Ngày 5-6 (08-10/12): Testing & Swagger

- [ ] Setup Swagger UI
  - Config `SwaggerConfig.java`
  - Add API documentation annotations

- [ ] Test với Postman:
  - Upload ảnh test
  - Verify response format
  - Test error cases (file quá lớn, sai format)

- [ ] Exception handling:
  - `GlobalExceptionHandler.java`
  - Custom error responses

### Ngày 7 (11/12): Polish & Documentation

- [ ] Code cleanup
- [ ] Write API documentation
- [ ] Test integration với Frontend (mock)
- [ ] Commit code
- [ ] **Demo API cho team**

---

## API Endpoints

```bash
POST /api/predict/cnn
POST /api/predict/resnet50
GET /actuator/health
GET /swagger-ui.html
```

---

## Output Deliverables

- Spring Boot API chạy port 8080
- Swagger UI: http://localhost:8080/swagger-ui.html
- Test passed với Postman

---

## Notes

- Backend GỌI Python Flask API (không load model trực tiếp)
- Temp uploads folder tự động cleanup
- CORS config cho frontend localhost:5173

---

**Status:** TODO → DOING → DONE ✓  
**Next:** Iteration 3 - Optimization & Bug fixes
