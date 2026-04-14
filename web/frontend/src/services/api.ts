import axios from 'axios';
import type {
  ScanTask,
  UploadResponse,
  PaginatedResponse,
  Vulnerability,
  ScanReport,
  Tutorial,
  VulnerableApp,
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:3080';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 300000, // 5 minutes for large file uploads
  headers: {
    'Content-Type': 'application/json',
  },
  maxContentLength: Infinity,
  maxBodyLength: Infinity,
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const scannerApi = {
  async uploadAPK(file: File): Promise<UploadResponse> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/api/v1/scans/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  async getScanTask(taskId: string): Promise<ScanTask> {
    const [taskResponse, vulnsResponse] = await Promise.all([
      api.get(`/api/v1/scans/${taskId}`),
      api.get(`/api/v1/scans/${taskId}/vulnerabilities`).catch(() => ({ data: [] })),
    ]);

    const taskData = taskResponse.data;
    const vulnsData = vulnsResponse.data;

    return {
      id: taskData.task_id,
      filename: taskData.filename,
      file_size: 0,
      file_hash: '',
      status: taskData.status,
      progress: taskData.progress,
      app_name: taskData.app_name,
      app_version: taskData.version_name,
      package_name: taskData.package_name,
      created_at: taskData.created_at,
      updated_at: taskData.completed_at || taskData.started_at || taskData.created_at,
      vulnerabilities: vulnsData.map((v: any) => ({
        id: v.id,
        title: v.title,
        description: v.description,
        severity: v.severity,
        cwe_id: v.cwe_id,
        cvss_score: v.cvss_score,
        recommendation: v.recommendation,
        location: v.location,
        scan_task_id: v.scan_task_id,
        created_at: v.created_at,
      })),
      reports: taskData.total_vulnerabilities > 0 ? [{
        id: `report-${taskData.task_id}`,
        format: 'json',
        total_vulnerabilities: taskData.total_vulnerabilities,
        critical_count: taskData.critical_count || 0,
        high_count: taskData.high_count || 0,
        medium_count: taskData.medium_count || 0,
        low_count: taskData.low_count || 0,
        info_count: taskData.info_count || 0,
        generated_at: taskData.completed_at || new Date().toISOString(),
        scan_task_id: taskData.task_id,
      }] : [],
    };
  },

  async getScanTasks(page = 1, pageSize = 10): Promise<PaginatedResponse<ScanTask>> {
    const response = await api.get('/api/v1/scans', {
      params: { page, page_size: pageSize },
    });
    const data = response.data;
    return {
      items: data.items.map((item: any) => ({
        id: item.task_id,
        filename: item.filename,
        file_size: 0,
        file_hash: '',
        status: item.status,
        progress: 100,
        app_name: item.app_name,
        app_version: '',
        package_name: item.package_name,
        created_at: item.created_at,
        updated_at: item.created_at,
        reports: item.total_vulnerabilities ? [{
          id: `report-${item.task_id}`,
          format: 'json',
          total_vulnerabilities: item.total_vulnerabilities,
          critical_count: 0,
          high_count: 0,
          medium_count: 0,
          low_count: 0,
          info_count: 0,
          generated_at: item.created_at,
          scan_task_id: item.task_id,
        }] : [],
      })),
      total: data.total,
      page: data.page,
      page_size: data.per_page,
      total_pages: data.total_pages,
    };
  },

  async deleteScanTask(taskId: string): Promise<void> {
    await api.delete(`/api/v1/scans/${taskId}`);
  },

  async getReport(taskId: string, format: string = 'json'): Promise<ScanReport> {
    const response = await api.get(`/api/v1/scans/${taskId}/report`, {
      params: { format },
    });
    return response.data;
  },

  async downloadReport(taskId: string, format: string): Promise<void> {
    const response = await api.get(`/api/v1/scans/${taskId}/report`, {
      params: { format },
      responseType: 'blob',
    });

    // 创建下载链接
    const blob = new Blob([response.data], { type: format === 'json' ? 'application/json' : 'text/html' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `scan-report-${taskId}.${format}`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  },

  async getVulnerabilities(taskId: string): Promise<Vulnerability[]> {
    const response = await api.get(`/api/v1/scans/${taskId}/vulnerabilities`);
    return response.data;
  },

  async checkHealth(): Promise<{ status: string }> {
    const response = await api.get('/health');
    return response.data;
  },
};

export const labApi = {
  async getTutorials(): Promise<Tutorial[]> {
    return [
      {
        id: 'm2',
        title: 'Insecure Data Storage',
        description: 'Learn how to identify and exploit insecure data storage vulnerabilities',
        category: 'OWASP Mobile Top 10',
        difficulty: 'beginner',
        duration: '45 min',
        modules: [],
      },
      {
        id: 'm4',
        title: 'Insecure Authentication',
        description: 'Learn how to bypass weak authentication mechanisms',
        category: 'OWASP Mobile Top 10',
        difficulty: 'intermediate',
        duration: '60 min',
        modules: [],
      },
    ];
  },

  async getTutorial(id: string): Promise<Tutorial | null> {
    const tutorials = await this.getTutorials();
    return tutorials.find((t) => t.id === id) || null;
  },

  async getVulnerableApps(): Promise<VulnerableApp[]> {
    return [
      {
        id: 'insecurebankv2',
        name: 'InsecureBankv2',
        description: 'Classic vulnerable Android app with various security flaws',
        vulnerabilities: ['Insecure Authentication', 'SQL Injection', 'Insecure Data Storage'],
        download_url: 'https://github.com/dineshshetty/Android-InsecureBankv2/releases',
      },
      {
        id: 'diva',
        name: 'DIVA - Damn Insecure and Vulnerable App',
        description: 'Vulnerable app designed for Android penetration testing practice',
        vulnerabilities: ['Insecure Logging', 'Hardcoded Secrets', 'Insecure Storage'],
        download_url: 'https://github.com/payatu/diva-android',
      },
      {
        id: 'sieve',
        name: 'Sieve',
        description: 'A password manager app with multiple vulnerabilities',
        vulnerabilities: ['Insecure Data Storage', 'Key Disclosure'],
        download_url: 'https://github.com/mwrlabs/sieve',
      },
    ];
  },
};

export const authApi = {
  async login(username: string, password: string): Promise<{ token: string; user: any }> {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          token: 'mock_token_' + Date.now(),
          user: { id: '1', username, email: username + '@example.com' },
        });
      }, 500);
    });
  },

  async logout(): Promise<void> {
    localStorage.removeItem('auth_token');
  },

  async getCurrentUser(): Promise<any> {
    const token = localStorage.getItem('auth_token');
    if (!token) return null;

    return {
      id: '1',
      username: 'demo',
      email: 'demo@example.com',
    };
  },
};

export default api;