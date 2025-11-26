# Iteration 1 - Tấn Lộc (27/11 - 04/12)

**Mục tiêu:** Image preview logic

---

## Checklist

### Ngày 1-3 (27-29/11): Setup & Preview Component

- [ ] Clone project về local
- [ ] Setup React environment (cùng với Quốc Anh)
- [ ] Tạo component: `ImagePreview.jsx`
  ```javascript
  // Hiển thị ảnh preview trước khi upload
  const [preview, setPreview] = useState(null);
  
  useEffect(() => {
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => setPreview(reader.result);
      reader.readAsDataURL(file);
    }
  }, [file]);
  ```

### Ngày 4-5 (30/11-01/12): Placeholder Result

- [ ] Tạo component: `ResultPlaceholder.jsx`
  - Skeleton loading khi đang predict
  - Animation effect
  - Placeholder cho confidence bar

### Ngày 6-7 (02-04/12): ResNet Notebook Prep

- [ ] Tạo file `notebooks/ResNet.ipynb`
- [ ] Research ResNet50 architecture
- [ ] Chuẩn bị code template:
  - Load pretrained ResNet50
  - Custom top layers
  - Data loading pipeline
- [ ] Đọc docs TensorFlow/Keras
- [ ] Commit notebook template

---

## Output Deliverables

- `ImagePreview.jsx` - Preview ảnh component
- `ResultPlaceholder.jsx` - Loading state component
- `notebooks/ResNet.ipynb` - Template sẵn sàng cho Iteration 2

---

## Notes

- Preview logic dùng FileReader API (client-side)
- KHÔNG gửi ảnh lên server trong Iteration 1 (chỉ preview)
- ResNet notebook chưa train, chỉ chuẩn bị structure

---

**Status:** TODO → DOING → DONE ✓  
**Next:** Iteration 2 - ResNet50 Training trên Kaggle
