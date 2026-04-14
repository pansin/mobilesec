export interface ScanTask {
  id: string;
  filename: string;
  file_size: number;
  file_hash: string;
  status: ScanStatus;
  progress: number;
  app_name?: string;
  app_version?: string;
  package_name?: string;
  created_at: string;
  updated_at: string;
  vulnerabilities?: Vulnerability[];
  reports?: ScanReport[];
}

export type ScanStatus =
  | 'pending'
  | 'uploading'
  | 'uploaded'
  | 'scanning'
  | 'analyzing'
  | 'generating_report'
  | 'completed'
  | 'failed';

export interface Vulnerability {
  id: string;
  title: string;
  description: string;
  severity: Severity;
  cwe_id?: string;
  cvss_score?: number;
  recommendation?: string;
  location?: string;
  evidence?: string;
  scan_task_id: string;
  created_at: string;
}

export type Severity = 'critical' | 'high' | 'medium' | 'low' | 'info';

export interface ScanReport {
  id: string;
  format: ReportFormat;
  file_path?: string;
  total_vulnerabilities: number;
  critical_count: number;
  high_count: number;
  medium_count: number;
  low_count: number;
  info_count: number;
  generated_at: string;
  scan_task_id: string;
}

export type ReportFormat = 'html' | 'pdf' | 'json';

export interface UploadResponse {
  task_id: string;
  filename: string;
  status: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface Tutorial {
  id: string;
  title: string;
  description: string;
  category: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  duration: string;
  modules: TutorialModule[];
}

export interface TutorialModule {
  id: string;
  title: string;
  content: string;
  exercises?: Exercise[];
}

export interface Exercise {
  id: string;
  title: string;
  description: string;
  type: 'reading' | 'practical' | 'quiz';
  app?: string;
  steps?: string[];
}

export interface VulnerableApp {
  id: string;
  name: string;
  description: string;
  vulnerabilities: string[];
  download_url: string;
}

export interface User {
  id: string;
  username: string;
  email: string;
  avatar?: string;
}

export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}