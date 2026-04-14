import { Shield, Upload, Activity, BookOpen, ChevronRight, CheckCircle, AlertTriangle, XCircle } from 'lucide-react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';

const stats = [
  { name: 'Total Scans', value: '127', change: '+12%', icon: Activity, color: 'text-blue-600', bg: 'bg-blue-50' },
  { name: 'Vulnerabilities Found', value: '892', change: '+5%', icon: AlertTriangle, color: 'text-orange-600', bg: 'bg-orange-50' },
  { name: 'Fixed Issues', value: '543', change: '+18%', icon: CheckCircle, color: 'text-green-600', bg: 'bg-green-50' },
  { name: 'Active Users', value: '48', change: '+3', icon: Shield, color: 'text-purple-600', bg: 'bg-purple-50' },
];

const recentScans = [
  { id: '1', name: 'app-release.apk', status: 'completed', severity: 'high', time: '2 hours ago' },
  { id: '2', name: 'banking-app.apk', status: 'scanning', severity: 'critical', time: '15 minutes ago' },
  { id: '3', name: 'test-app-debug.apk', status: 'completed', severity: 'low', time: '1 day ago' },
  { id: '4', name: 'social-app.apk', status: 'failed', severity: 'info', time: '3 hours ago' },
];

export function DashboardPage() {
  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-1">Welcome back! Here's what's happening.</p>
        </div>
        <Link
          to="/scanner"
          className="inline-flex items-center space-x-2 bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors"
        >
          <Upload className="h-5 w-5" />
          <span>New Scan</span>
        </Link>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <motion.div
              key={stat.name}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-white rounded-lg shadow-sm border border-gray-200 p-6"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                  <p className="text-2xl font-bold text-gray-900 mt-1">{stat.value}</p>
                  <p className="text-sm text-green-600 mt-1">{stat.change}</p>
                </div>
                <div className={`${stat.bg} p-3 rounded-lg`}>
                  <Icon className={`h-6 w-6 ${stat.color}`} />
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Scans */}
        <div className="lg:col-span-2 bg-white rounded-lg shadow-sm border border-gray-200">
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold text-gray-900">Recent Scans</h2>
              <Link
                to="/scans"
                className="text-sm text-primary-600 hover:text-primary-700 inline-flex items-center"
              >
                View all <ChevronRight className="h-4 w-4 ml-1" />
              </Link>
            </div>
          </div>
          <div className="divide-y divide-gray-200">
            {recentScans.map((scan) => (
              <div key={scan.id} className="p-6 hover:bg-gray-50">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                      scan.status === 'completed'
                        ? 'bg-green-100'
                        : scan.status === 'scanning'
                        ? 'bg-blue-100'
                        : 'bg-red-100'
                    }`}>
                      {scan.status === 'completed' ? (
                        <CheckCircle className="h-5 w-5 text-green-600" />
                      ) : scan.status === 'scanning' ? (
                        <Activity className="h-5 w-5 text-blue-600 animate-spin" />
                      ) : (
                        <XCircle className="h-5 w-5 text-red-600" />
                      )}
                    </div>
                    <div>
                      <p className="font-medium text-gray-900">{scan.name}</p>
                      <p className="text-sm text-gray-500">{scan.time}</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-4">
                    <span
                      className={`px-2 py-1 text-xs font-medium rounded-full ${
                        scan.severity === 'critical'
                          ? 'bg-red-100 text-red-800'
                          : scan.severity === 'high'
                          ? 'bg-orange-100 text-orange-800'
                          : 'bg-blue-100 text-blue-800'
                      }`}
                    >
                      {scan.severity}
                    </span>
                    <Link
                      to={`/scans/${scan.id}`}
                      className="text-primary-600 hover:text-primary-700"
                    >
                      <ChevronRight className="h-5 w-5" />
                    </Link>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="space-y-6">
          {/* Quick Actions */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
            <div className="space-y-3">
              <Link
                to="/scanner"
                className="flex items-center space-x-3 p-3 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <div className="bg-primary-100 p-2 rounded-lg">
                  <Upload className="h-5 w-5 text-primary-600" />
                </div>
                <div>
                  <p className="font-medium text-gray-900">Upload APK</p>
                  <p className="text-sm text-gray-500">Scan a new application</p>
                </div>
              </Link>
              <Link
                to="/tutorials"
                className="flex items-center space-x-3 p-3 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <div className="bg-green-100 p-2 rounded-lg">
                  <BookOpen className="h-5 w-5 text-green-600" />
                </div>
                <div>
                  <p className="font-medium text-gray-900">Learn</p>
                  <p className="text-sm text-gray-500">Browse tutorials</p>
                </div>
              </Link>
              <Link
                to="/vulnapps"
                className="flex items-center space-x-3 p-3 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <div className="bg-orange-100 p-2 rounded-lg">
                  <Shield className="h-5 w-5 text-orange-600" />
                </div>
                <div>
                  <p className="font-medium text-gray-900">VulnApps</p>
                  <p className="text-sm text-gray-500">Practice targets</p>
                </div>
              </Link>
            </div>
          </div>

          {/* Vulnerability Distribution */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Severity Distribution</h2>
            <div className="space-y-4">
              <div>
                <div className="flex items-center justify-between mb-1">
                  <span className="text-sm font-medium text-gray-700">Critical</span>
                  <span className="text-sm text-gray-500">12</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-red-500 h-2 rounded-full" style={{ width: '15%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex items-center justify-between mb-1">
                  <span className="text-sm font-medium text-gray-700">High</span>
                  <span className="text-sm text-gray-500">45</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-orange-500 h-2 rounded-full" style={{ width: '35%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex items-center justify-between mb-1">
                  <span className="text-sm font-medium text-gray-700">Medium</span>
                  <span className="text-sm text-gray-500">67</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-yellow-500 h-2 rounded-full" style={{ width: '55%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex items-center justify-between mb-1">
                  <span className="text-sm font-medium text-gray-700">Low</span>
                  <span className="text-sm text-gray-500">98</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-blue-500 h-2 rounded-full" style={{ width: '75%' }}></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}