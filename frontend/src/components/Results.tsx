import { CheckCircle, XCircle, Video, Volume2 } from 'lucide-react';
import { AnalysisResult } from '../types';

interface ResultsProps {
  result: AnalysisResult;
}

export function Results({ result }: ResultsProps) {
  const isReal = result.verdict === 'Real';
  const hasVideoAnalysis = result.videoConfidence > 0;
  
  const CircularProgress = ({ value, label, icon }: { value: number; label: string; icon: React.ReactNode }) => {
    const circumference = 2 * Math.PI * 45;
    const strokeDasharray = circumference;
    const strokeDashoffset = circumference - (value * circumference);
    
    return (
      <div className="flex flex-col items-center space-y-3">
        <div className="relative w-24 h-24">
          <svg className="w-24 h-24 transform -rotate-90" viewBox="0 0 100 100">
            <circle
              cx="50"
              cy="50"
              r="45"
              stroke="currentColor"
              strokeWidth="8"
              fill="transparent"
              className="text-gray-200 dark:text-gray-700"
            />
            <circle
              cx="50"
              cy="50"
              r="45"
              stroke="currentColor"
              strokeWidth="8"
              fill="transparent"
              strokeDasharray={strokeDasharray}
              strokeDashoffset={strokeDashoffset}
              className={`transition-all duration-1000 ease-out ${
                value > 0.7 ? 'text-green-500' : value > 0.4 ? 'text-yellow-500' : 'text-red-500'
              }`}
              strokeLinecap="round"
            />
          </svg>
          
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="text-center">
              <div className="w-8 h-8 mx-auto mb-1 text-gray-600 dark:text-gray-300">
                {icon}
              </div>
              <span className="text-lg font-bold text-gray-800 dark:text-white">
                {Math.round(value * 100)}%
              </span>
            </div>
          </div>
        </div>
        
        <div className="text-center">
          <p className="font-medium text-gray-800 dark:text-white">{label}</p>
          <p className="text-sm text-gray-500 dark:text-gray-400">Confidence</p>
        </div>
      </div>
    );
  };

  return (
    <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-2xl p-8 border border-white/20 shadow-xl">
      <div className="text-center mb-8">
        <div className={`inline-flex items-center space-x-3 px-6 py-4 rounded-2xl ${
          isReal 
            ? 'bg-green-50 dark:bg-green-900/30 text-green-700 dark:text-green-300' 
            : 'bg-red-50 dark:bg-red-900/30 text-red-700 dark:text-red-300'
        }`}>
          {isReal ? (
            <CheckCircle className="w-8 h-8" />
          ) : (
            <XCircle className="w-8 h-8" />
          )}
          <div>
            <h2 className="text-2xl font-bold">
              {result.verdict}
            </h2>
            <p className="text-sm opacity-80">
              Detection Complete
            </p>
          </div>
        </div>
      </div>

      <div className={`grid gap-8 mb-6 ${hasVideoAnalysis ? 'grid-cols-1 md:grid-cols-2' : 'grid-cols-1 justify-items-center'}`}>
        {hasVideoAnalysis && (
          <CircularProgress
            value={result.videoConfidence}
            label="Video Analysis"
            icon={<Video className="w-full h-full" />}
          />
        )}
        
        <CircularProgress
          value={result.audioConfidence}
          label="Audio Analysis"
          icon={<Volume2 className="w-full h-full" />}
        />
      </div>

      <div className="bg-gray-50 dark:bg-gray-700/50 rounded-xl p-4">
        <div className="flex justify-between items-center text-sm">
          <span className="text-gray-600 dark:text-gray-300">Processing Time:</span>
          <span className="font-medium text-gray-800 dark:text-white">
            {result.processingTime.toFixed(1)}s
          </span>
        </div>
      </div>
    </div>
  );
}