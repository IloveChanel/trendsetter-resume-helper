
'use client';

import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

interface ResumeUploadProps {
  onUpload: (text: string) => void;
}

export default function ResumeUpload({ onUpload }: ResumeUploadProps) {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      const content = e.target?.result as string;
      console.log('File content:', content); // DEBUG: Check this in console
      onUpload(content);
    };
    reader.readAsText(file);
  }, [onUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt']
    },
    multiple: false
  });

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-navy-900">Upload Your Resume</h3>
      
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
          ${isDragActive 
            ? 'border-primary-500 bg-primary-50' 
            : 'border-navy-300 hover:border-primary-400 hover:bg-primary-25'
          }`}
      >
        <input {...getInputProps()} />
        <div className="space-y-2">
          <div className="text-4xl">📄</div>
          <p className="text-navy-700 font-medium">
            {isDragActive ? 'Drop your resume here...' : 'Drop your resume here, or click to select'}
          </p>
          <p className="text-sm text-navy-500">
            Supports PDF, DOC, DOCX, or TXT files
          </p>
        </div>
      </div>
    </div>
  );
}