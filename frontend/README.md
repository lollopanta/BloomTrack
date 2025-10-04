# BloomTracker Frontend

A modern React frontend for the BloomTracker environmental forecasting platform, built with TypeScript, TailwindCSS, and interactive data visualizations.

## 🚀 Features

- **Modern React Architecture**: Built with React 18, TypeScript, and Vite
- **Interactive Data Visualization**: Charts, maps, and time-series analysis
- **Responsive Design**: Mobile-first approach with TailwindCSS
- **Real-time API Integration**: Seamless connection to FastAPI backend
- **Beautiful Animations**: Smooth transitions with Framer Motion
- **Geospatial Mapping**: Interactive maps with Mapbox GL JS
- **Predictive Analytics**: ML model selection and comparison

## 🛠️ Tech Stack

- **React 18** - Modern React with hooks and concurrent features
- **TypeScript** - Type-safe development
- **Vite** - Fast build tool and dev server
- **TailwindCSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **Framer Motion** - Animation library
- **Recharts** - Data visualization
- **React Leaflet** - Interactive maps with OpenStreetMap
- **Axios** - HTTP client for API requests
- **Lucide React** - Beautiful icons

## 📦 Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd frontend
   ```

2. **Install dependencies:**

   ```bash
   npm install
   ```

3. **Set up environment variables:**

   ```bash
   cp env.example .env
   ```

   Edit `.env` with your configuration:

   ```
   VITE_API_BASE_URL=http://localhost:8000
   ```

4. **Start the development server:**

   ```bash
   npm run dev
   ```

5. **Open your browser:**
   Navigate to `http://localhost:3000`

## 🏗️ Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Navbar.tsx      # Navigation component
│   ├── Hero.tsx        # Hero section
│   ├── DatasetCard.tsx # Dataset cards
│   ├── Chart.tsx       # Data visualization
│   ├── MapView.tsx     # Interactive maps
│   └── Loader.tsx      # Loading states
├── pages/              # Page components
│   ├── Home.tsx        # Home page
│   ├── DatasetDetail.tsx # Dataset detail page
│   └── About.tsx       # About page
├── api/                # API integration
│   ├── client.ts       # Axios configuration
│   └── bloomtracker.ts # API functions
├── types/              # TypeScript types
│   └── index.ts        # Type definitions
├── utils/              # Utility functions
│   └── index.ts        # Helper functions
├── App.tsx             # Main app component
├── main.tsx           # App entry point
└── index.css          # Global styles
```

## 🎨 Design System

### Colors

- **Primary**: Green (`#22c55e`) - Nature and growth
- **Secondary**: Sky Blue (`#3b82f6`) - Technology and innovation
- **Accent**: Indigo (`#6366f1`) - Trust and reliability

### Typography

- **Font**: Inter - Modern, readable sans-serif
- **Weights**: 300, 400, 500, 600, 700, 800, 900

### Components

- **Cards**: Rounded corners, subtle shadows, hover effects
- **Buttons**: Gradient backgrounds, smooth transitions
- **Forms**: Clean inputs with focus states
- **Charts**: Interactive with tooltips and legends

## 📊 Data Visualization

### Charts

- **Line Charts**: Time series data with current vs predicted
- **Area Charts**: Filled areas for trend visualization
- **Interactive Tooltips**: Detailed data on hover
- **Responsive Design**: Adapts to different screen sizes

### Maps

- **Mapbox Integration**: High-quality satellite imagery
- **Layer Toggles**: Switch between current and predicted data
- **Interactive Markers**: Click to explore data points
- **Geospatial Overlays**: Visualize data coverage

## 🔌 API Integration

The frontend integrates with the BloomTracker FastAPI backend:

### Endpoints Used

- `GET /data/{dataset}` - Fetch dataset information
- `GET /predict/{dataset}` - Get predictions
- `GET /health` - Health check
- `POST /predict/train` - Train models

### Error Handling

- Network error recovery
- Loading states
- User-friendly error messages
- Retry mechanisms

## 🎭 Animations

### Framer Motion

- **Page Transitions**: Smooth route changes
- **Component Animations**: Staggered reveals
- **Hover Effects**: Interactive feedback
- **Loading States**: Engaging spinners

### Performance

- **Optimized Animations**: 60fps smooth transitions
- **Reduced Motion**: Respects user preferences
- **Lazy Loading**: Components load on demand

## 📱 Responsive Design

### Breakpoints

- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

### Mobile Features

- **Touch Gestures**: Swipe navigation
- **Optimized Charts**: Touch-friendly interactions
- **Collapsible Navigation**: Mobile menu
- **Fast Loading**: Optimized for mobile networks

## 🚀 Deployment

### Build for Production

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

### Environment Variables

- `VITE_API_BASE_URL` - Backend API URL
- `VITE_MAPBOX_TOKEN` - Mapbox access token

## 🧪 Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Code Quality

- **TypeScript**: Strict type checking
- **ESLint**: Code linting and formatting
- **Prettier**: Code formatting (recommended)
- **Husky**: Git hooks for quality checks

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is part of the BloomTracker system for environmental data processing and analysis.

## 🆘 Support

For support and questions:

- Check the documentation
- Open an issue on GitHub
- Contact the development team

---

Built with ❤️ for environmental science and data-driven decision making.
