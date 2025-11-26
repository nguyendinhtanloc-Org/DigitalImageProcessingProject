# Frontend - ReactJS Application

## Mô tả

Frontend cho dự án Pneumonia Detection, xây dựng bằng **ReactJS 18** và **TailwindCSS**, cung cấp giao diện để upload ảnh X-ray và hiển thị kết quả dự đoán.

## Công nghệ

- **React 18.x** - UI Library
- **Vite** - Build tool & Dev server
- **TailwindCSS** - Utility-first CSS
- **Axios** - HTTP Client
- **React Router** - Routing

## Cấu trúc

```
frontend/
├── public/
│   └── vite.svg
├── src/
│   ├── components/           # Reusable components
│   │   ├── UploadImage.jsx
│   │   ├── ResultDisplay.jsx
│   │   ├── GradCAM.jsx
│   │   └── Header.jsx
│   ├── pages/               # Pages/Views
│   │   ├── Home.jsx
│   │   └── About.jsx
│   ├── services/            # API services
│   │   └── apiService.js
│   ├── utils/               # Utilities
│   │   └── helpers.js
│   ├── App.jsx              # Main App component
│   ├── main.jsx             # Entry point
│   └── index.css            # Global styles
├── .eslintrc.cjs
├── tailwind.config.js
├── vite.config.js
├── package.json
└── README.md
```

## Setup và Chạy

### Prerequisites

- Node.js 18+ và npm/yarn

### 1. Cài đặt dependencies

```bash
cd frontend
npm install
# hoặc
yarn install
```

### 2. Cấu hình environment

Tạo file `.env.local`:

```bash
VITE_API_URL=http://localhost:8080/api
```

### 3. Chạy development server

```bash
npm run dev
# hoặc
yarn dev
```

App chạy tại: `http://localhost:5173`

## Components

### UploadImage Component

Component để upload ảnh X-ray.

**Usage:**
```jsx
import UploadImage from './components/UploadImage';

function Home() {
  const handleUploadSuccess = (result) => {
    console.log('Prediction:', result);
  };

  return <UploadImage onUploadSuccess={handleUploadSuccess} />;
}
```

### ResultDisplay Component

Hiển thị kết quả dự đoán.

**Props:**
- `prediction`: String - "NORMAL" hoặc "PNEUMONIA"
- `confidence`: Number - 0.0 to 1.0
- `model`: String - "cnn" hoặc "resnet50"

**Usage:**
```jsx
<ResultDisplay 
  prediction="PNEUMONIA"
  confidence={0.9542}
  model="cnn"
/>
```

### GradCAM Component

Hiển thị heatmap Grad-CAM.

**Props:**
- `imageUrl`: String - URL của ảnh gốc
- `heatmapUrl`: String - URL của heatmap

## API Integration

### apiService.js

```javascript
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL;

export const predictImage = async (file, model = 'cnn') => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('model', model);

  const response = await axios.post(
    `${API_URL}/predict`,
    formData,
    {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }
  );

  return response.data;
};

export const getGradCAM = async (file, model = 'resnet50') => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('model', model);

  const response = await axios.post(
    `${API_URL}/gradcam`,
    formData,
    {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }
  );

  return response.data;
};
```

## Styling với TailwindCSS

### Cấu hình

**tailwind.config.js:**
```javascript
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3B82F6',
        secondary: '#10B981',
        danger: '#EF4444',
      },
    },
  },
  plugins: [],
}
```

### Example

```jsx
<div className="container mx-auto px-4 py-8">
  <h1 className="text-3xl font-bold text-gray-800 mb-6">
    Pneumonia Detection
  </h1>
  
  <div className="bg-white rounded-lg shadow-md p-6">
    {/* Content */}
  </div>
</div>
```

## Testing

### Unit Tests

```bash
npm run test
```

### E2E Tests (nếu setup)

```bash
npm run test:e2e
```

## Build cho Production

```bash
npm run build
# hoặc
yarn build
```

Build output sẽ ở trong thư mục `dist/`.

### Preview production build

```bash
npm run preview
```

## Docker

**Dockerfile:**
```dockerfile
FROM node:18-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Build và chạy:**
```bash
docker build -t pneumonia-frontend .
docker run -p 80:80 pneumonia-frontend
```

## Development

### Code Style

- Sử dụng **ESLint** cho linting
- Sử dụng **Prettier** cho formatting
- Tuân theo **Airbnb JavaScript Style Guide**

### Format code

```bash
npm run format
```

### Lint code

```bash
npm run lint
```

## Deployment

### Deploy lên Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Deploy lên Netlify

```bash
# Install Netlify CLI
npm i -g netlify-cli

# Deploy
netlify deploy --prod --dir=dist
```

## Troubleshooting

### Lỗi CORS

Đảm bảo backend đã config CORS cho phép origin từ frontend.

### Environment variables không load

- File `.env.local` phải có prefix `VITE_`
- Restart dev server sau khi thay đổi `.env`

### Build bị lỗi

```bash
# Clear cache và reinstall
rm -rf node_modules dist
npm install
npm run build
```

## Resources

- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [TailwindCSS Documentation](https://tailwindcss.com/)
- [Axios Documentation](https://axios-http.com/)

---

**Liên hệ:** Frontend Team - frontend@example.com
