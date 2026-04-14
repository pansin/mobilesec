import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AuthProvider } from './hooks/useAuth';
import { Sidebar } from './components/Sidebar';
import { DashboardPage } from './pages/DashboardPage';
import { ScannerPage } from './pages/ScannerPage';
import { ScansPage } from './pages/ScansPage';
import { ScanDetailPage } from './pages/ScanDetailPage';
import { TutorialsPage } from './pages/TutorialsPage';
import { VulnAppsPage } from './pages/VulnAppsPage';
import './index.css';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: false,
    },
  },
});

const router = createBrowserRouter([
  {
    path: '/',
    element: <Sidebar />,
    children: [
      {
        path: '',
        element: <DashboardPage />,
      },
      {
        path: 'scanner',
        element: <ScannerPage />,
      },
      {
        path: 'scans',
        element: <ScansPage />,
      },
      {
        path: 'scans/:taskId',
        element: <ScanDetailPage />,
      },
      {
        path: 'tutorials',
        element: <TutorialsPage />,
      },
      {
        path: 'vulnapps',
        element: <VulnAppsPage />,
      },
      {
        path: 'reports',
        element: <div className="p-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-6">Reports</h1>
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <p className="text-gray-600">
              This feature is under development. Reports management will be available soon.
            </p>
          </div>
        </div>,
      },
    ],
  },
]);

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <RouterProvider router={router} />
      </AuthProvider>
    </QueryClientProvider>
  );
}