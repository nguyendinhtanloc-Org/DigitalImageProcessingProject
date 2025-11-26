# Iteration 3 - Quốc Anh (11/12 - 18/12)

**Mục tiêu:** Frontend-Backend Integration

---

## Checklist

### Ngày 1-3 (11-13/12): Real API Integration

- [ ] Update `services/api.js`:
  ```javascript
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

- [ ] Replace mock data với real API calls
- [ ] Handle loading states
- [ ] Handle errors từ backend
- [ ] Test integration

### Ngày 4-5 (14-16/12): UI/UX Polish

- [ ] Responsive design:
  - Mobile (< 768px)
  - Tablet (768-1024px)
  - Desktop (> 1024px)

- [ ] Loading animations:
  - Skeleton loading
  - Progress indicators
  - Smooth transitions

- [ ] Error handling UI:
  - Toast notifications
  - Error boundaries
  - User-friendly messages

- [ ] Accessibility:
  - Alt texts
  - ARIA labels
  - Keyboard navigation

### Ngày 6-7 (17-18/12): Testing & Demo

- [ ] End-to-end testing:
  - Upload ảnh → Predict → Display result
  - Test cả CNN & ResNet50
  - Test error cases

- [ ] Browser testing:
  - Chrome
  - Firefox
  - Safari

- [ ] Performance optimization:
  - Lazy loading
  - Code splitting
  - Image optimization

- [ ] **Final demo với full stack**

---

## Output Deliverables

- Production-ready frontend
- Connected với backend API
- Responsive & accessible UI

---

**Status:** TODO → DOING → DONE ✓
