# Iteration 1 - Quốc Anh (27/11 - 04/12)

**Mục tiêu:** Frontend skeleton với TailwindCSS

---

## Checklist

### Ngày 1-2 (27-28/11): Setup Project

- [ ] Setup React + Vite
  ```bash
  cd frontend
  npm create vite@latest . -- --template react
  npm install
  ```
- [ ] Cài TailwindCSS
  ```bash
  npm install -D tailwindcss postcss autoprefixer
  npx tailwindcss init -p
  ```
- [ ] Config `tailwind.config.js`
- [ ] Test dev server: `npm run dev`

### Ngày 3-4 (29-30/11): Layout & Components

- [ ] Tạo layout cơ bản
  - Header với title
  - Main content area
  - Footer (optional)

- [ ] Component: `UploadImage.jsx`
  - Input file upload
  - Preview ảnh sau khi chọn
  - Validation: chỉ accept .jpg, .png

- [ ] Component: `ModelSelector.jsx`
  - Radio button: CNN / ResNet50
  - State management

### Ngày 5-6 (01-03/12): Mock Data & Styling

- [ ] Component: `ResultDisplay.jsx`
  - Hiển thị prediction: Normal/Pneumonia
  - Confidence score: 95.2%
  - Styling với TailwindCSS

- [ ] Tạo mock API: `services/api.js`
  ```javascript
  export const predictImage = async (file, model) => {
    // Fake delay
    await new Promise(r => setTimeout(r, 1000));
    return {
      prediction: "Pneumonia",
      confidence: 95.2
    };
  };
  ```

- [ ] Test toàn bộ flow với mock data

### Ngày 7 (04/12): Polish & Demo

- [ ] Responsive design (mobile, tablet, desktop)
- [ ] Loading state (spinner khi "predict")
- [ ] Error handling UI
- [ ] Commit code lên GitHub
- [ ] **Demo UI cho team**

---

## Output Deliverables

- Frontend chạy được tại `localhost:5173`
- 3 components: UploadImage, ModelSelector, ResultDisplay
- Mock API hoạt động

---

## Tech Stack

- React 18 + Vite
- TailwindCSS
- React Hooks (useState, useEffect)

---

**Status:** TODO → DOING → DONE ✓  
**Next:** Iteration 2 - CNN Training & React Components nâng cao
