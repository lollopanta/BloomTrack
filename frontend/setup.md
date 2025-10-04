# BloomTracker Frontend Setup Guide

## 🚀 Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Environment Setup

```bash
# Copy environment template
cp env.example .env

# Edit .env file with your settings
VITE_API_BASE_URL=http://localhost:8000
```

### 3. Start Development Server

```bash
npm run dev
```

### 4. Open in Browser

Navigate to `http://localhost:3000`

## 🔧 Configuration

### Backend API

Make sure your BloomTracker backend is running on `http://localhost:8000`

### Map Configuration

The application uses OpenStreetMap tiles which don't require an API key.

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/     # UI Components
│   ├── pages/         # Page Components
│   ├── api/           # API Integration
│   ├── types/         # TypeScript Types
│   ├── utils/         # Utility Functions
│   ├── App.tsx        # Main App
│   └── main.tsx       # Entry Point
├── public/            # Static Assets
├── package.json       # Dependencies
├── tailwind.config.js # TailwindCSS Config
├── vite.config.ts     # Vite Config
└── README.md          # Documentation
```

## 🎨 Features Implemented

✅ **Modern React Architecture**

- React 18 with TypeScript
- Vite for fast development
- TailwindCSS for styling

✅ **Interactive Components**

- Responsive navigation
- Animated hero section
- Dataset cards with hover effects
- Interactive charts and maps

✅ **Data Visualization**

- Recharts for time series
- Mapbox GL JS for maps
- Real-time data updates
- Model comparison features

✅ **API Integration**

- Axios HTTP client
- Error handling
- Loading states
- Type-safe API calls

✅ **Responsive Design**

- Mobile-first approach
- Touch-friendly interactions
- Optimized for all devices

## 🚀 Deployment

### Build for Production

```bash
npm run build
```

### Preview Production

```bash
npm run preview
```

### Deploy to Vercel/Netlify

The build output in `dist/` can be deployed to any static hosting service.

## 🎯 Next Steps

1. **Get Mapbox Token**: Sign up and get your token
2. **Start Backend**: Ensure your FastAPI backend is running
3. **Customize**: Modify colors, fonts, and branding
4. **Deploy**: Build and deploy to your hosting platform

## 🆘 Troubleshooting

### Common Issues

- **Port conflicts**: Change port in `vite.config.ts`
- **API errors**: Check backend is running on correct port
- **Map not loading**: Verify Mapbox token is correct
- **Build errors**: Check TypeScript types and imports

### Development Tips

- Use browser dev tools for debugging
- Check console for API errors
- Use React DevTools for component debugging
- Monitor network tab for API calls

---

**Ready to forecast the future of Earth from space! 🌍🛰️**
