import { useCallback, useState } from 'react';
import { Upload, Video, X, FileVideo, Music } from 'lucide-react';
import { UploadedFile } from '../types';

interface FileUploadProps {
  onFileUpload: (file: UploadedFile) => void;
  uploadedFile: UploadedFile | null;
  onRemoveFile: () => void;
}

export function FileUpload({ onFileUpload, uploadedFile, onRemoveFile }: FileUploadProps) {
  const [isDragOver, setIsDragOver] = useState(false);

  const isValidMediaFile = (file: File): boolean => {
    const validVideoTypes = [
      'video/mp4',
      'video/avi',
      'video/mov',
      'video/quicktime',
      'video/x-msvideo',
      'video/webm',
      'video/ogg'
    ];
    
    const validAudioTypes = [
      'audio/wav',
      'audio/wave',
      'audio/x-wav',
      'audio/mpeg',
      'audio/mp3'
    ];
    
    const validExtensions = ['.mp4', '.avi', '.mov', '.webm', '.ogg', '.wav', '.mp3'];
    const fileExtension = file.name.toLowerCase().substring(file.name.lastIndexOf('.'));
    
    return validVideoTypes.includes(file.type) || 
           validAudioTypes.includes(file.type) || 
           validExtensions.includes(fileExtension);
  };

  const isVideoFile = (file: File): boolean => {
    const videoTypes = ['video/mp4', 'video/avi', 'video/mov', 'video/quicktime', 'video/x-msvideo', 'video/webm', 'video/ogg'];
    const videoExtensions = ['.mp4', '.avi', '.mov', '.webm', '.ogg'];
    const fileExtension = file.name.toLowerCase().substring(file.name.lastIndexOf('.'));
    
    return videoTypes.includes(file.type) || videoExtensions.includes(fileExtension);
  };

  const isAudioFile = (file: File): boolean => {
    const audioTypes = ['audio/wav', 'audio/wave', 'audio/x-wav', 'audio/mpeg', 'audio/mp3'];
    const audioExtensions = ['.wav', '.mp3'];
    const fileExtension = file.name.toLowerCase().substring(file.name.lastIndexOf('.'));
    
    return audioTypes.includes(file.type) || audioExtensions.includes(fileExtension);
  };

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    
    const files = Array.from(e.dataTransfer.files);
    const mediaFile = files.find(file => isValidMediaFile(file));
    
    if (mediaFile) {
      processFile(mediaFile);
    } else {
      alert('Please upload a valid media file (MP4, AVI, MOV, WebM, OGG, WAV, MP3)');
    }
  }, []);

  const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (isValidMediaFile(file)) {
        processFile(file);
      } else {
        alert('Please upload a valid media file (MP4, AVI, MOV, WebM, OGG, WAV, MP3)');
        e.target.value = ''; // Reset the input
      }
    }
  }, []);

  const processFile = (file: File) => {
    const preview = URL.createObjectURL(file);
    onFileUpload({
      file,
      preview,
      name: file.name,
      size: file.size
    });
  };

  const formatFileSize = (bytes: number) => {
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    if (bytes === 0) return '0 Bytes';
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
  };

  if (uploadedFile) {
    const isVideo = isVideoFile(uploadedFile.file);
    const isAudio = isAudioFile(uploadedFile.file);

    return (
      <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-2xl p-6 border border-white/20 shadow-xl">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-800 dark:text-white">
            Uploaded {isVideo ? 'Video' : 'Audio'} File
          </h3>
          <button
            onClick={onRemoveFile}
            className="p-2 hover:bg-red-100 dark:hover:bg-red-900/30 rounded-lg transition-colors"
          >
            <X className="w-4 h-4 text-red-500" />
          </button>
        </div>
        
        <div className="flex items-center space-x-4">
          <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
            {isVideo ? (
              <Video className="w-8 h-8 text-white" />
            ) : (
              <Music className="w-8 h-8 text-white" />
            )}
          </div>
          
          <div className="flex-1 min-w-0">
            <p className="font-medium text-gray-800 dark:text-white truncate">
              {uploadedFile.name}
            </p>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              {formatFileSize(uploadedFile.size)}
            </p>
          </div>
        </div>

        {/* Media Preview */}
        <div className="mt-4">
          {isVideo ? (
            <video
              src={uploadedFile.preview}
              controls
              className="w-full max-h-64 rounded-lg bg-black"
              preload="metadata"
            >
              Your browser does not support the video tag.
            </video>
          ) : isAudio ? (
            <div className="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4">
              <audio
                src={uploadedFile.preview}
                controls
                className="w-full"
                preload="metadata"
              >
                Your browser does not support the audio tag.
              </audio>
            </div>
          ) : null}
        </div>
      </div>
    );
  }

  return (
    <div
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      className={`relative bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-2xl p-8 border-2 border-dashed transition-all duration-300 ${
        isDragOver
          ? 'border-blue-500 bg-blue-50/80 dark:bg-blue-900/20'
          : 'border-gray-300 dark:border-gray-600 hover:border-blue-400 dark:hover:border-blue-500'
      }`}
    >
      <div className="text-center space-y-4">
        <div className="w-16 h-16 mx-auto bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
          <FileVideo className="w-8 h-8 text-white" />
        </div>
        
        <div>
          <h3 className="text-xl font-semibold text-gray-800 dark:text-white mb-2">
            Upload Media File
          </h3>
          <p className="text-gray-600 dark:text-gray-300 mb-4">
            Drag and drop your video or audio file here, or click to browse
          </p>
        </div>
        
        <div className="flex flex-col sm:flex-row gap-4 items-center justify-center">
          <label className="cursor-pointer bg-gradient-to-r from-blue-500 to-purple-600 text-white px-6 py-3 rounded-xl font-medium hover:from-blue-600 hover:to-purple-700 transition-all duration-300 flex items-center space-x-2 hover:scale-105">
            <Upload className="w-4 h-4" />
            <span>Choose File</span>
            <input
              type="file"
              accept="video/*,audio/*,.mp4,.avi,.mov,.webm,.ogg,.wav,.mp3"
              onChange={handleFileSelect}
              className="hidden"
            />
          </label>
          
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Supports MP4, AVI, MOV, WebM, OGG, WAV, MP3 files
          </p>
        </div>
      </div>
    </div>
  );
}