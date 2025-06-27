import axios from 'axios';
import React, { useState, useEffect } from 'react';
import { Shield, Zap, Server } from 'lucide-react';
import { FileUpload } from '../components/FileUpload';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { Results } from '../components/Results';
import { Navbar } from '../components/Navbar';
import { UploadedFile, AnalysisResult, HistoryItem } from '../types';
import { useAuth } from '../hooks/useAuth';

export function DetectionPage() {
  const { user } = useAuth();
  const [uploadedFile, setUploadedFile] = useState<UploadedFile | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [progress, setProgress] = useState(0);
  const [backendStatus, setBackendStatus] = useState<'checking' | 'healthy' | 'unreachable'>('checking');

  // Check backend health on component mount
  useEffect(() => {
    const checkBackendHealth = async () => {
      try {
        await axios.get('http://localhost:8000/api/health');
        setBackendStatus('healthy');
      } catch (error) {
        setBackendStatus('unreachable');
        console.error('Backend connection error:', error);
      }
    };

    checkBackendHealth();
  }, []);

  const handleFileUpload = (file: UploadedFile) => {
    setUploadedFile(file);
    setAnalysisResult(null);
  };

  const handleRemoveFile = () => {
    setUploadedFile(null);
    setAnalysisResult(null);
    if (uploadedFile?.preview) {
      URL.revokeObjectURL(uploadedFile.preview);
    }
  };

  const saveToHistory = (result: AnalysisResult) => {
    if (!uploadedFile || !user) return;

    const historyItem: HistoryItem = {
      id: Date.now().toString(),
      filename: uploadedFile.name,
      uploadTime: new Date(),
      result: result,
      userId: user.id
    };

    const existingHistory = JSON.parse(localStorage.getItem('analysisHistory') || '[]');
    const updatedHistory = [historyItem, ...existingHistory];
    localStorage.setItem('analysisHistory', JSON.stringify(updatedHistory));
  };

  const isAudioFile = (file: File): boolean => {
    const audioTypes = ['audio/wav', 'audio/wave', 'audio/x-wav', 'audio/mpeg', 'audio/mp3'];
    const audioExtensions = ['.wav', '.mp3'];
    const fileExtension = file.name.toLowerCase().substring(file.name.lastIndexOf('.'));
    
    return audioTypes.includes(file.type) || audioExtensions.includes(fileExtension);
  };

  const handleAnalyze = async () => {
    if (!uploadedFile) return;

    setIsAnalyzing(true);
    setProgress(0);
    const startTime = Date.now();

    // Simulate analysis with realistic progress
    const progressInterval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 95) return prev;
        return prev + Math.random() * 15;
      });
    }, 200);

    // Simulate analysis time (3-5 seconds)
    const analysisTime = 3000 + Math.random() * 2000;
    
    setTimeout(() => {
      clearInterval(progressInterval);
      setProgress(100);
      
      // Generate realistic results based on file type
      const isAudio = isAudioFile(uploadedFile.file);
      
      let videoConfidence = 0;
      let audioConfidence = 0;
      
      if (isAudio) {
        audioConfidence = 0.3 + Math.random() * 0.7;
        videoConfidence = 0;
      } else {
        videoConfidence = 0.3 + Math.random() * 0.7;
        audioConfidence = 0.2 + Math.random() * 0.8;
      }
      
      const avgConfidence = isAudio ? audioConfidence : (videoConfidence + audioConfidence) / 2;
      
      const result: AnalysisResult = {
        videoConfidence,
        audioConfidence,
        verdict: avgConfidence > 0.6 ? 'Real' : 'Fake',
        processingTime: (Date.now() - startTime) / 1000
      };

      setTimeout(() => {
        setAnalysisResult(result);
        saveToHistory(result);
        setIsAnalyzing(false);
        setProgress(0);
      }, 500);
    }, analysisTime);
  };

  const handleNewAnalysis = () => {
    setAnalysisResult(null);
  };

  // Status indicator colors
  const statusColors = {
    checking: 'text-yellow-500',
    healthy: 'text-green-500',
    unreachable: 'text-red-500'
  };

  const statusMessages = {
    checking: 'Checking backend...',
    healthy: 'Backend connected',
    unreachable: 'Backend unreachable'
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-purple-900 transition-colors duration-300">
      <Navbar />
      
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center space-x-3 mb-4">
            <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
              <Shield className="w-6 h-6 text-white" />
            </div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              DeepGuard AI
            </h1>
          </div>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Advanced deepfake detection powered by cutting-edge AI technology
          </p>
        </div>

        <div className="max-w-4xl mx-auto space-y-8">
          {/* File Upload */}
          <FileUpload
            onFileUpload={handleFileUpload}
            uploadedFile={uploadedFile}
            onRemoveFile={handleRemoveFile}
          />

          {/* Analyze Button */}
          {uploadedFile && !isAnalyzing && !analysisResult && (
            <div className="text-center">
              <button
                onClick={handleAnalyze}
                disabled={backendStatus !== 'healthy'}
                className={`bg-gradient-to-r from-blue-500 to-purple-600 text-white px-8 py-4 rounded-xl font-semibold text-lg transition-all duration-300 flex items-center space-x-3 mx-auto hover:scale-105 shadow-lg ${
                  backendStatus !== 'healthy' ? 'opacity-50 cursor-not-allowed' : 'hover:from-blue-600 hover:to-purple-700'
                }`}
              >
                <Zap className="w-5 h-5" />
                <span>Detect Deepfake</span>
              </button>
              {backendStatus !== 'healthy' && (
                <p className="text-red-500 mt-2">
                  {backendStatus === 'unreachable'
                    ? 'Backend unavailable - check your connection'
                    : 'Verifying backend connection...'}
                </p>
              )}
            </div>
          )}

          {/* Loading State */}
          {isAnalyzing && (
            <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-2xl border border-white/20 shadow-xl">
              <LoadingSpinner progress={progress} />
            </div>
          )}

          {/* Results */}
          {analysisResult && (
            <>
              <Results result={analysisResult} />
              <div className="text-center">
                <button
                  onClick={handleNewAnalysis}
                  className="bg-gradient-to-r from-gray-500 to-gray-600 text-white px-6 py-3 rounded-xl font-medium hover:from-gray-600 hover:to-gray-700 transition-all duration-300"
                >
                  Analyze New File
                </button>
              </div>
            </>
          )}
        </div>

        {/* Footer with backend status */}
        <div className="text-center mt-16 text-gray-500 dark:text-gray-400">
          <p>© 2025 DeepGuard AI. Protecting authenticity in the digital age.</p>
          <div className="mt-2 flex items-center justify-center space-x-1">
            <Server className={`w-4 h-4 ${statusColors[backendStatus]}`} />
            <span className={`text-sm ${statusColors[backendStatus]}`}>
              {statusMessages[backendStatus]}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
