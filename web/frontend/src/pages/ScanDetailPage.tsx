import { useParams, Link } from 'react-router-dom';
import { useState } from 'react';
import {
  FileText,
  AlertTriangle,
  ChevronLeft,
  Download,
  Shield,
  Code,
  Lock,
  Globe,
  Filter,
} from 'lucide-react';
import { useQuery } from '@tanstack/react-query';
import { scannerApi } from '../services/api';
import { formatDateTime, formatBytes, getStatusText } from '../utils';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

export function ScanDetailPage() {
  const { taskId } = useParams<{ taskId: string }>();
  const [filterSeverity, setFilterSeverity] = useState<string>('all');

  const { data: scanTask, isLoading, error } = useQuery({
    queryKey: ['scan', taskId],
    queryFn: () => scannerApi.getScanTask(taskId!),
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error || !scanTask) {
    return (
      <div className="text-center py-12">
        <AlertTriangle className="h-12 w-12 text-red-500 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">Failed to load scan details</h3>
        <p className="text-gray-500">The scan task may not exist or has been deleted</p>
      </div>
    );
  }

  const filteredVulnerabilities = filterSeverity === 'all'
    ? scanTask.vulnerabilities
    : scanTask.vulnerabilities?.filter(v => v.severity === filterSeverity);

  const report = scanTask.reports?.[0] || {
    critical_count: 0,
    high_count: 0,
    medium_count: 0,
    low_count: 0,
    info_count: 0,
    total_vulnerabilities: 0,
  };

  const severityData = [
    { name: 'Critical', count: report.critical_count, color: '#ef4444' },
    { name: 'High', count: report.high_count, color: '#f97316' },
    { name: 'Medium', count: report.medium_count, color: '#f59e0b' },
    { name: 'Low', count: report.low_count, color: '#3b82f6' },
    { name: 'Info', count: report.info_count, color: '#10b981' },
  ].filter((item) => item.count > 0);

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'critical':
        return <Shield className="h-5 w-5 text-red-500" />;
      case 'high':
        return <AlertTriangle className="h-5 w-5 text-orange-500" />;
      case 'medium':
        return <Code className="h-5 w-5 text-yellow-500" />;
      case 'low':
        return <Lock className="h-5 w-5 text-blue-500" />;
      default:
        return <Globe className="h-5 w-5 text-green-500" />;
    }
  };

  const getSeverityBadgeColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'bg-red-100 text-red-800';
      case 'high':
        return 'bg-orange-100 text-orange-800';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'low':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-green-100 text-green-800';
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-8">
        <Link
          to="/scans"
          className="inline-flex items-center space-x-2 text-gray-600 hover:text-gray-900 mb-4"
        >
          <ChevronLeft className="h-4 w-4" />
          <span>Back to Scans</span>
        </Link>
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Scan Details</h1>
            <p className="text-gray-600 mt-1">{taskId}</p>
          </div>
          <div className="flex items-center space-x-4">
            <button
              onClick={() => scannerApi.downloadReport(taskId!, 'json')}
              className="inline-flex items-center space-x-2 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <Download className="h-5 w-5" />
              <span>Download Report (JSON)</span>
            </button>
            <button
              onClick={() => scannerApi.downloadReport(taskId!, 'html')}
              className="inline-flex items-center space-x-2 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <FileText className="h-5 w-5" />
              <span>Download Report (HTML)</span>
            </button>
          </div>
        </div>
      </div>

      {/* Status Header */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-6">
            <div className="flex items-center space-x-2">
              <div className={`w-4 h-4 rounded-full ${
                scanTask.status === 'completed' ? 'bg-green-500' : 'bg-blue-500'
              }`}></div>
              <span className="text-sm font-medium text-gray-900">
                {getStatusText(scanTask.status)}
              </span>
              {scanTask.status === 'completed' && (
                <span className="text-sm text-green-600">
                  ({report.total_vulnerabilities} vulnerabilities)
                </span>
              )}
            </div>
          </div>
          <div className="text-sm text-gray-500">
            Created: {formatDateTime(scanTask.created_at)}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
        {/* App Info */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">App Information</h2>
          <div className="space-y-4">
            <div>
              <p className="text-sm font-medium text-gray-500">Application Name</p>
              <p className="text-sm text-gray-900">{scanTask.app_name}</p>
            </div>
            <div>
              <p className="text-sm font-medium text-gray-500">Package Name</p>
              <p className="text-sm text-gray-900 font-mono">{scanTask.package_name}</p>
            </div>
            <div>
              <p className="text-sm font-medium text-gray-500">Version</p>
              <p className="text-sm text-gray-900">{scanTask.app_version}</p>
            </div>
            <div>
              <p className="text-sm font-medium text-gray-500">File Size</p>
              <p className="text-sm text-gray-900">{formatBytes(scanTask.file_size)}</p>
            </div>
            <div>
              <p className="text-sm font-medium text-gray-500">File Hash</p>
              <p className="text-sm text-gray-900 font-mono">{scanTask.file_hash}</p>
            </div>
          </div>
        </div>

        {/* Vulnerability Chart */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 lg:col-span-2">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Vulnerability Distribution</h2>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={severityData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#3b82f6">
                {severityData.map((entry, index) => (
                  <rect key={`cell-${index}`} fill={entry.color} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Vulnerabilities */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 mb-8">
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-center justify-between flex-wrap gap-4">
            <h2 className="text-lg font-semibold text-gray-900">Vulnerabilities</h2>
            <div className="flex items-center space-x-2">
              <Filter className="h-4 w-4 text-gray-500" />
              <select
                value={filterSeverity}
                onChange={(e) => setFilterSeverity(e.target.value)}
                className="border border-gray-300 rounded-lg px-3 py-1.5 text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              >
                <option value="all">All Severities ({scanTask.vulnerabilities?.length || 0})</option>
                <option value="critical">Critical ({report.critical_count})</option>
                <option value="high">High ({report.high_count})</option>
                <option value="medium">Medium ({report.medium_count})</option>
                <option value="low">Low ({report.low_count})</option>
                <option value="info">Info ({report.info_count})</option>
              </select>
            </div>
          </div>
        </div>
        <div className="divide-y divide-gray-200">
          {!filteredVulnerabilities || filteredVulnerabilities.length === 0 ? (
            <div className="p-6 text-center text-gray-500">
              {filterSeverity === 'all'
                ? 'No vulnerabilities found. The scan is still in progress or no issues were detected.'
                : `No ${filterSeverity} severity vulnerabilities found.`}
            </div>
          ) : filteredVulnerabilities.map((vuln) => (
            <div key={vuln.id} className="p-6 hover:bg-gray-50 transition-colors">
              <div className="flex items-start space-x-4">
                <div className="flex-shrink-0">
                  {getSeverityIcon(vuln.severity)}
                </div>
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-2 flex-wrap gap-2">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      getSeverityBadgeColor(vuln.severity)
                    }`}>
                      {vuln.severity.toUpperCase()}
                    </span>
                    {vuln.cwe_id && (
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                        {vuln.cwe_id}
                      </span>
                    )}
                    {vuln.cvss_score && (
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                        CVSS: {vuln.cvss_score}
                      </span>
                    )}
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">{vuln.title}</h3>
                  <p className="text-gray-600 mb-4 whitespace-pre-wrap">{vuln.description}</p>
                  {vuln.recommendation && vuln.recommendation.trim() && (
                    <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg">
                      <p className="text-sm font-medium text-green-900 mb-1">💡 Recommendation:</p>
                      <p className="text-sm text-green-700">{vuln.recommendation}</p>
                    </div>
                  )}
                  {vuln.location && (
                    <div className="p-3 bg-gray-50 border border-gray-200 rounded-lg">
                      <p className="text-sm font-medium text-gray-900 mb-1">📍 Location:</p>
                      <p className="text-sm text-gray-600 font-mono break-all">{vuln.location}</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}