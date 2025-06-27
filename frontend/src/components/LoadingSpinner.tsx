import { Loader2, Eye } from 'lucide-react';

interface LoadingSpinnerProps {
  progress: number;
}

export function LoadingSpinner({ progress }: LoadingSpinnerProps) {
  return (
    <div className="flex flex-col items-center justify-center p-8 space-y-6">
      <div className="relative">
        <div className="w-24 h-24 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 p-1">
          <div className="w-full h-full rounded-full bg-white dark:bg-gray-900 flex items-center justify-center">
            <Eye className="w-8 h-8 text-blue-500 animate-pulse" />
          </div>
        </div>
        <Loader2 className="absolute inset-0 w-24 h-24 text-blue-500 animate-spin" />
      </div>
      
      <div className="text-center space-y-3">
        <h3 className="text-xl font-semibold text-gray-800 dark:text-white">
          Analyzing Video...
        </h3>
        <p className="text-gray-600 dark:text-gray-300">
          Advanced AI is processing your content
        </p>
        
        <div className="w-64 bg-gray-200 dark:bg-gray-700 rounded-full h-2 overflow-hidden">
          <div 
            className="h-full bg-gradient-to-r from-blue-500 to-purple-600 transition-all duration-300 ease-out"
            style={{ width: `${progress}%` }}
          />
        </div>
        
        <p className="text-sm text-gray-500 dark:text-gray-400">
          {progress}% Complete
        </p>
      </div>
    </div>
  );
}