// API Response Types
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  metadata?: any;
  message?: string;
  error?: string;
}

export interface DatasetData {
  description: string;
  files: any[];
  total_files: number;
  data_type: string;
}

export interface PredictionData {
  predicted_values: number[];
  timestamps: string[];
  model_used: string;
  source: string;
}

export interface DatasetInfo {
  name: string;
  displayName: string;
  description: string;
  icon: string;
  color: string;
  route: string;
}

// Component Props Types
export interface DatasetCardProps {
  dataset: DatasetInfo;
  onClick: (dataset: string) => void;
}

export interface MapViewProps {
  data?: DatasetData;
  predictions?: PredictionData;
  dataset: string;
}

export interface ChartProps {
  data: any[];
  currentData?: any[];
  predictedData?: any[];
  title: string;
}

// Navigation Types
export interface NavItem {
  label: string;
  href: string;
  icon?: string;
}

// API Client Types
export interface ApiClient {
  get: (url: string) => Promise<any>;
  post: (url: string, data?: any) => Promise<any>;
  put: (url: string, data?: any) => Promise<any>;
  delete: (url: string) => Promise<any>;
}
