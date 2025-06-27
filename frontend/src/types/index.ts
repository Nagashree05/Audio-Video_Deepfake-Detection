export interface UploadedFile {
  file: File;
  preview: string;
  name: string;
  size: number;
}

export interface AnalysisResult {
  videoConfidence: number;
  audioConfidence: number;
  verdict: 'Real' | 'Fake';
  processingTime: number;
}

export interface ThemeContextType {
  isDark: boolean;
  toggleTheme: () => void;
}

export interface User {
  id: string;
  name: string;
  email: string;
}

export interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  signup: (name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
}

export interface HistoryItem {
  id: string;
  filename: string;
  uploadTime: Date;
  result: AnalysisResult;
  userId: string;
}

export interface ValidationErrors {
  name?: string;
  email?: string;
  password?: string;
  confirmPassword?: string;
}