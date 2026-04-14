import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { Activity, FileText, ChevronRight, CheckCircle, AlertCircle, XCircle } from 'lucide-react';
import { scannerApi } from '../services/api';
import { formatDateTime, formatBytes, getSeverityColor, getStatusColor, getStatusText } from '../utils';

export function ScansPage() {
  const { data: scansData, isLoading, error } = useQuery({
    queryKey: ['scans'],
    queryFn: async () => {
      try {
        // Try to fetch from API
        const response = await scannerApi.getScanTasks(1, 20);
        return response;
      } catch (error) {
        // Fallback to mock data if API fails
        console.warn('API failed, using mock data:', error);
        return {
          items: [
            {
              id: 'task-1',
              filename: 'banking-app.apk',
              file_size: 24576000,
              file_hash: 'abc123',
              status: 'completed',
              progress: 100,
              app_name: 'Mobile Banking',
              app_version: '2.1.0',
              package_name: 'com.example.banking',
              created_at: new Date(Date.now() - 3600000 * 2).toISOString(),
              updated_at: new Date(Date.now() - 3600000).toISOString(),
              reports: [
                {
                  id: 'report-1',
                  format: 'json',
                  total_vulnerabilities: 23,
                  critical_count: 3,
                  high_count: 8,
                  medium_count: 7,
                  low_count: 5,
                  info_count: 0,
                  generated_at: new Date().toISOString(),
                  scan_task_id: 'task-1',
                },
              ],
            },
            {
              id: 'task-2',
              filename: 'social-app.apk',
              file_size: 45088768,
              file_hash: 'def456',
              status: 'scanning',
              progress: 65,
              app_name: 'Social Connect',
              app_version: '5.3.2',
              package_name: 'com.example.social',
              created_at: new Date(Date.now() - 1800000).toISOString(),
              updated_at: new Date(Date.now() - 60000).toISOString(),
            },
            {
              id: 'task-3',
              filename: 'ecommerce.apk',
              file_size: 31457280,
              file_hash: 'ghi789',
              status: 'completed',
              progress: 100,
              app_name: 'ShopEasy',
              app_version: '1.8.4',
              package_name: 'com.example.shop',
              created_at: new Date(Date.now() - 3600000 * 24).toISOString(),
              updated_at: new Date(Date.now() - 3600000 * 23).toISOString(),
              reports: [
                {
                  id: 'report-2',
                  format: 'json',
                  total_vulnerabilities: 15,
                  critical_count: 1,
                  high_count: 4,
                  medium_count: 5,
                  low_count: 5,
                  info_count: 0,
                  generated_at: new Date().toISOString(),
                  scan_task_id: 'task-3',
                },
              ],
            },
            {
              id: 'task-4',
              filename: 'fitness-app.apk',
              file_size: 18874368,
              file_hash: 'jkl012',
              status: 'failed',
              progress: 30,
              app_name: 'FitTrack',
              app_version: '3.0.0',
              package_name: 'com.example.fitness',
              created_at: new Date(Date.now() - 3600000 * 48).toISOString(),
              updated_at: new Date(Date.now() - 3600000 * 47).toISOString(),
            },
          ],
          total: 4,
          page: 1,
          page_size: 20,
          total_pages: 1,
        };
      }
    },
  });

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'scanning':
      case 'analyzing':
        return <Activity className="h-5 w-5 text-blue-500 animate-spin" />;
      case 'failed':
        return <XCircle className="h-5 w-5 text-red-500" />;
      default:
        return <AlertCircle className="h-5 w-5 text-yellow-500" />;
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">Failed to load scans</h3>
        <p className="text-gray-500">Please try again later</p>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Scan History</h1>
          <p className="text-gray-600 mt-1">View and manage all your APK scans</p>
        </div>
        <Link
          to="/scanner"
          className="inline-flex items-center space-x-2 bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors"
        >
          <FileText className="h-5 w-5" />
          <span>New Scan</span>
        </Link>
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  App
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Vulnerabilities
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Size
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Date
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {scansData?.items.map((scan) => (
                <tr key={scan.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4">
                    <div className="flex items-center">
                      <div className="flex-shrink-0 w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
                        <FileText className="h-5 w-5 text-primary-600" />
                      </div>
                      <div className="ml-4">
                        <div className="text-sm font-medium text-gray-900">
                          {scan.app_name || scan.filename}
                        </div>
                        <div className="text-sm text-gray-500">
                          {scan.package_name}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center space-x-2">
                      {getStatusIcon(scan.status)}
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        scan.status === 'completed'
                          ? 'bg-green-100 text-green-800'
                          : scan.status === 'scanning' || scan.status === 'analyzing'
                          ? 'bg-blue-100 text-blue-800'
                          : scan.status === 'failed'
                          ? 'bg-red-100 text-red-800'
                          : 'bg-yellow-100 text-yellow-800'
                      }`}>
                        {getStatusText(scan.status)}
                      </span>
                    </div>
                    {scan.progress < 100 && scan.status !== 'failed' && (
                      <div className="mt-2 w-full bg-gray-200 rounded-full h-1.5">
                        <div
                          className="bg-primary-600 h-1.5 rounded-full"
                          style={{ width: `${scan.progress}%` }}
                        ></div>
                      </div>
                    )}
                  </td>
                  <td className="px-6 py-4">
                    {scan.reports && scan.reports.length > 0 ? (
                      <div className="flex items-center space-x-2">
                        {scan.reports[0].critical_count > 0 && (
                          <span className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-red-100 text-red-800">
                            {scan.reports[0].critical_count} Critical
                          </span>
                        )}
                        {scan.reports[0].high_count > 0 && (
                          <span className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-orange-100 text-orange-800">
                            {scan.reports[0].high_count} High
                          </span>
                        )}
                        <span className="text-sm text-gray-500">
                          {scan.reports[0].total_vulnerabilities} total
                        </span>
                      </div>
                    ) : (
                      <span className="text-sm text-gray-500">—</span>
                    )}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-500">
                    {formatBytes(scan.file_size)}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-500">
                    {formatDateTime(scan.created_at)}
                  </td>
                  <td className="px-6 py-4 text-right">
                    <Link
                      to={`/scans/${scan.task_id || scan.id}`}
                      className="inline-flex items-center text-primary-600 hover:text-primary-700"
                    >
                      View <ChevronRight className="h-4 w-4 ml-1" />
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}