
'use client';

import React from 'react';

interface JobInputProps {
  jobTitle: string;
  jobDescription: string;
  onJobTitleChange: (value: string) => void;
  onJobDescriptionChange: (value: string) => void;
}

export default function JobInput({
  jobTitle,
  jobDescription,
  onJobTitleChange,
  onJobDescriptionChange,
}: JobInputProps) {
  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-navy-900">Job Details</h3>
      
      {/* Job Title */}
      <div>
        <label htmlFor="jobTitle" className="block text-sm font-medium text-navy-700 mb-2">
          Job Title (Optional)
        </label>
        <input
          id="jobTitle"
          type="text"
          value={jobTitle}
          onChange={(e) => onJobTitleChange(e.target.value)}
          placeholder="e.g., Senior Software Engineer"
          className="w-full px-3 py-2 border border-navy-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        />
      </div>

      {/* Job Description */}
      <div>
        <label htmlFor="jobDescription" className="block text-sm font-medium text-navy-700 mb-2">
          Job Description *
        </label>
        <textarea
          id="jobDescription"
          value={jobDescription}
          onChange={(e) => {
            console.log('Job description changed:', e.target.value); // DEBUG
            onJobDescriptionChange(e.target.value);
          }}
          placeholder="Paste the full job description here..."
          rows={8}
          className="w-full px-3 py-2 border border-navy-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-vertical"
          required
        />
      </div>
    </div>
  );
}
