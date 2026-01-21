'use client';

import React, { useState } from 'react';
import ResumeUpload from '@/components/ResumeUpload';
import JobInput from '@/components/JobInput';
import Results from '@/components/Results';

export default function Home() {
  const [resumeText, setResumeText] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [jobTitle, setJobTitle] = useState('');
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!resumeText || !jobDescription) {
      alert('Please upload a resume and enter a job description');
      return;
    }

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('resume_text', resumeText);
      formData.append('job_description', jobDescription);
      if (jobTitle) {
        formData.append('job_title', jobTitle);
      }

      const response = await fetch('http://localhost:8000/api/match-job', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Analysis failed');
      }

      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Error analyzing resume:', error);
      alert('Error analyzing resume. Please make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-navy-50 via-white to-primary-50">
      {/* Header */}
      <header className="bg-white border-b border-navy-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-navy-900">
                🚀 Trendsetter Resume Helper
              </h1>
              <p className="text-sm text-navy-600 mt-1">
                Beat ATS Bots & Rank Your Resume at the Top
              </p>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        {!results && (
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-navy-900 mb-4">
              Optimize Your Resume for ATS
            </h2>
            <p className="text-lg text-navy-600 max-w-2xl mx-auto">
              Upload your resume and paste a job description to get instant analysis,
              keyword matching, and optimization suggestions.
            </p>
          </div>
        )}

        {/* Main Content */}
        {!results ? (
          <div className="grid md:grid-cols-2 gap-8 mb-8">
            {/* Left Column - Resume Upload */}
            <div className="bg-white rounded-lg shadow-lg p-6 border border-navy-100">
              <ResumeUpload onUpload={setResumeText} />
            </div>

            {/* Right Column - Job Input */}
            <div className="bg-white rounded-lg shadow-lg p-6 border border-navy-100">
              <JobInput
                jobTitle={jobTitle}
                jobDescription={jobDescription}
                onJobTitleChange={setJobTitle}
                onJobDescriptionChange={setJobDescription}
              />
            </div>
          </div>
        ) : (
          <Results
            results={results}
            onReset={() => {
              setResults(null);
              setResumeText('');
              setJobDescription('');
              setJobTitle('');
            }}
          />
        )}

        {/* Analyze Button */}
        {!results && (
          <div className="flex justify-center">
            <button
              onClick={handleAnalyze}
              disabled={loading || !resumeText || !jobDescription}
              className={`px-12 py-4 rounded-lg text-white font-semibold text-lg shadow-lg transition-all
                ${
                  loading || !resumeText || !jobDescription
                    ? 'bg-navy-300 cursor-not-allowed'
                    : 'bg-primary-600 hover:bg-primary-700 hover:shadow-xl transform hover:-translate-y-0.5'
                }`}
            >
              {loading ? (
                <span className="flex items-center gap-2">
                  <svg
                    className="animate-spin h-5 w-5"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    ></circle>
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                  Analyzing...
                </span>
              ) : (
                '🔍 Analyze Resume'
              )}
            </button>
          </div>
        )}

        {/* Features Section */}
        {!results && (
          <div className="mt-16 grid md:grid-cols-3 gap-8">
            <div className="text-center p-6">
              <div className="text-4xl mb-4">🤖</div>
              <h3 className="text-xl font-semibold text-navy-900 mb-2">
                ATS Compatibility
              </h3>
              <p className="text-navy-600">
                Check for ATS-killer issues like tables, graphics, and complex formatting
              </p>
            </div>
            <div className="text-center p-6">
              <div className="text-4xl mb-4">🔑</div>
              <h3 className="text-xl font-semibold text-navy-900 mb-2">
                Keyword Matching
              </h3>
              <p className="text-navy-600">
                Find missing keywords and get suggestions on where to add them
              </p>
            </div>
            <div className="text-center p-6">
              <div className="text-4xl mb-4">💡</div>
              <h3 className="text-xl font-semibold text-navy-900 mb-2">
                Smart Optimization
              </h3>
              <p className="text-navy-600">
                Get actionable suggestions to improve your resume score
              </p>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-navy-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 text-center text-navy-600">
          <p>&copy; 2024 Trendsetter Resume Helper. Beat the ATS bots! 🚀</p>
        </div>
      </footer>
    </div>
  );
}
