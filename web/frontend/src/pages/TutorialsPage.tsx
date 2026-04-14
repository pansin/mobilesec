import { useQuery } from '@tanstack/react-query';
import { BookOpen, ChevronRight, Clock, BarChart3, Lock, Shield } from 'lucide-react';
import { Link } from 'react-router-dom';
import { labApi } from '../services/api';

export function TutorialsPage() {
  const { data: tutorials, isLoading } = useQuery({
    queryKey: ['tutorials'],
    queryFn: () => labApi.getTutorials(),
  });

  const learningPaths = [
    {
      id: 'beginner',
      title: 'Beginner Path',
      description: 'Start here if you are new to Android security',
      duration: '0-3 months',
      modules: [
        { id: 1, title: 'Android Security Basics', completed: true },
        { id: 2, title: 'Static Analysis Fundamentals', completed: true },
        { id: 3, title: 'Insecure Data Storage', inProgress: true },
        { id: 4, title: 'Insecure Authentication', upcoming: true },
      ],
    },
    {
      id: 'intermediate',
      title: 'Intermediate Path',
      description: 'Build on your foundational knowledge',
      duration: '3-6 months',
      modules: [
        { id: 1, title: 'Network Analysis', upcoming: true },
        { id: 2, title: 'Frida Fundamentals', upcoming: true },
        { id: 3, title: 'Advanced Frida Scripting', upcoming: true },
      ],
    },
    {
      id: 'advanced',
      title: 'Advanced Path',
      description: 'Master advanced Android security techniques',
      duration: '6-12 months',
      modules: [
        { id: 1, title: 'Reverse Engineering', upcoming: true },
        { id: 2, title: 'Mobile Forensics', upcoming: true },
        { id: 3, title: 'Exploit Development', upcoming: true },
      ],
    },
  ];

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
        <h1 className="text-3xl font-bold text-gray-900">Tutorials</h1>
        <p className="text-gray-600 mt-1">Learn Android security with structured tutorials</p>
      </div>

      {/* Learning Paths */}
      <div className="mb-12">
        <h2 className="text-2xl font-semibold text-gray-900 mb-6">Learning Paths</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {learningPaths.map((path) => (
            <div key={path.id} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">{path.title}</h3>
                <span className="text-sm text-gray-500">{path.duration}</span>
              </div>
              <p className="text-gray-600 mb-6">{path.description}</p>
              <div className="space-y-2 mb-6">
                {path.modules.map((module) => (
                  <div key={module.id} className="flex items-center justify-between text-sm">
                    <span className={`${module.upcoming ? 'text-gray-400' : 'text-gray-700'}`}>
                      {module.title}
                    </span>
                    {module.completed && (
                      <span className="text-green-600">✓</span>
                    )}
                    {module.inProgress && (
                      <span className="text-primary-600 animate-pulse">...</span>
                    )}
                  </div>
                ))}
              </div>
              <Link
                to={`/tutorials/path/${path.id}`}
                className="inline-flex items-center text-primary-600 hover:text-primary-700"
              >
                Start Learning <ChevronRight className="h-4 w-4 ml-1" />
              </Link>
            </div>
          ))}
        </div>
      </div>

      {/* Individual Tutorials */}
      <div>
        <h2 className="text-2xl font-semibold text-gray-900 mb-6">All Tutorials</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {tutorials?.map((tutorial) => (
            <Link
              key={tutorial.id}
              to={`/tutorials/${tutorial.id}`}
              className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between mb-4">
                <div className={`p-3 rounded-lg ${
                  tutorial.difficulty === 'beginner'
                    ? 'bg-green-100'
                    : tutorial.difficulty === 'intermediate'
                    ? 'bg-blue-100'
                    : 'bg-purple-100'
                }`}>
                  <BookOpen className={`h-6 w-6 ${
                    tutorial.difficulty === 'beginner'
                      ? 'text-green-600'
                      : tutorial.difficulty === 'intermediate'
                      ? 'text-blue-600'
                      : 'text-purple-600'
                  }`} />
                </div>
                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                  tutorial.difficulty === 'beginner'
                    ? 'bg-green-100 text-green-800'
                    : tutorial.difficulty === 'intermediate'
                    ? 'bg-blue-100 text-blue-800'
                    : 'bg-purple-100 text-purple-800'
                }`}>
                  {tutorial.difficulty}
                </span>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">{tutorial.title}</h3>
              <p className="text-gray-600 text-sm mb-4">{tutorial.description}</p>
              <div className="flex items-center justify-between text-sm text-gray-500">
                <span className="flex items-center">
                  <Clock className="h-4 w-4 mr-1" />
                  {tutorial.duration}
                </span>
                <span className="text-primary-600 hover:text-primary-700">
                  Read more <ChevronRight className="h-4 w-4 inline" />
                </span>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}