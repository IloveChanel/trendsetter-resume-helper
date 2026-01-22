'use client';

import React from 'react';

interface JobInputProps {
  jobTitle: string;
  jobDescription: string;
  onJobTitleChange: (title: string) => void;
  onJobDescriptionChange: (description: string) => void;
}

export default function JobInput({
  jobTitle,
  jobDescription,
  onJobTitleChange,
  onJobDescriptionChange,
}: JobInputProps) {
  return (
    <div>
      <h2 className="text-xl font-semibold text-navy-900 mb-4">
        💼 Job Description
      </h2>
      
      <div className="space-y-4">
        <div>
          <label htmlFor="jobTitle" className="block text-sm font-medium text-navy-700 mb-2">
            Job Title (Optional)
          </label>
          <input
            id="jobTitle"
            type="text"
            value={jobTitle}
            onChange={(e) => onJobTitleChange(e.target.value)}
            placeholder="e.g., Senior Full Stack Developer"
            className="w-full px-4 py-2 border border-navy-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
        </div>

        <div>
          <label htmlFor="jobDescription" className="block text-sm font-medium text-navy-700 mb-2">
            Job Description
          </label>
          <textarea
            id="jobDescription"
            value={jobDescription}
            onChange={(e) => onJobDescriptionChange(e.target.value)}
            placeholder="Paste the job description here..."
            rows={12}
            className="w-full px-4 py-2 border border-navy-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
          />
          <p className="text-xs text-navy-500 mt-2">
            Include requirements, skills, and responsibilities
          </p>
        </div>

        <div>
          <label htmlFor="roleType" className="block text-sm font-medium text-navy-700 mb-2">
            Role Type
          </label>
          <select
            id="roleType"
            className="w-full px-4 py-2 border border-navy-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="Full Stack">Full Stack</option>
            <option value="Frontend">Frontend</option>
            <option value="Backend">Backend</option>
            <option value="Other">Other</option>
          </select>
        </div>
      </div>
    </div>
  );
}
