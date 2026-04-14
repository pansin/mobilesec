import { useQuery } from '@tanstack/react-query';
import { Shield, Download, ChevronRight, AlertTriangle, BookOpen, ExternalLink } from 'lucide-react';
import { labApi } from '../services/api';

export function VulnAppsPage() {
  const { data: vulnApps, isLoading } = useQuery({
    queryKey: ['vulnApps'],
    queryFn: () => labApi.getVulnerableApps(),
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Vulnerable Apps</h1>
        <p className="text-gray-600 mt-1">Practice your skills on intentionally vulnerable Android apps</p>
      </div>

      {/* Info Banner */}
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-8">
        <div className="flex items-start">
          <AlertTriangle className="h-5 w-5 text-yellow-600 mt-0.5 mr-3" />
          <div>
            <h3 className="text-sm font-medium text-yellow-800">Important</h3>
            <p className="text-sm text-yellow-700 mt-1">
              These apps are intentionally vulnerable. Never install them on personal devices.
              Use only in controlled test environments.
            </p>
          </div>
        </div>
      </div>

      {/* Vulnerable Apps Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {vulnApps?.map((app) => (
          <div key={app.id} className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
            <div className="p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="bg-red-100 p-3 rounded-lg">
                  <Shield className="h-6 w-6 text-red-600" />
                </div>
                <a
                  href={app.download_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center px-3 py-1.5 bg-primary-600 text-white text-sm rounded-lg hover:bg-primary-700 transition-colors"
                >
                  <Download className="h-4 w-4 mr-1" />
                  Download
                </a>
              </div>

              <h2 className="text-xl font-semibold text-gray-900 mb-2">{app.name}</h2>
              <p className="text-gray-600 mb-4">{app.description}</p>

              <div className="mb-4">
                <h3 className="text-sm font-medium text-gray-900 mb-2">Vulnerabilities:</h3>
                <div className="flex flex-wrap gap-2">
                  {app.vulnerabilities.map((vuln, index) => (
                    <span
                      key={index}
                      className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-orange-100 text-orange-800"
                    >
                      {vuln}
                    </span>
                  ))}
                </div>
              </div>

              <div className="flex items-center space-x-4 pt-4 border-t border-gray-200">
                <button className="inline-flex items-center text-primary-600 hover:text-primary-700">
                  <BookOpen className="h-4 w-4 mr-1" />
                  View Tutorial
                </button>
                <a
                  href={app.download_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center text-gray-600 hover:text-gray-900"
                >
                  <ExternalLink className="h-4 w-4 mr-1" />
                  Source
                </a>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Quick Start Guide */}
      <div className="mt-12 bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Start Guide</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <div className="flex items-center justify-center w-10 h-10 bg-primary-100 rounded-lg mb-3">
              <span className="text-primary-600 font-semibold">1</span>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">Download</h3>
            <p className="text-gray-600 text-sm">Select and download a vulnerable app from the list above.</p>
          </div>
          <div>
            <div className="flex items-center justify-center w-10 h-10 bg-primary-100 rounded-lg mb-3">
              <span className="text-primary-600 font-semibold">2</span>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">Install</h3>
            <p className="text-gray-600 text-sm">Install the app in your sandbox environment or emulator.</p>
          </div>
          <div>
            <div className="flex items-center justify-center w-10 h-10 bg-primary-100 rounded-lg mb-3">
              <span className="text-primary-600 font-semibold">3</span>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">Practice</h3>
            <p className="text-gray-600 text-sm">Follow the tutorials to exploit vulnerabilities and learn!</p>
          </div>
        </div>
      </div>
    </div>
  );
}