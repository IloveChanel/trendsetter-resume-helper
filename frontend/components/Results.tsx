'use client';

import React from 'react';

interface ResultsProps {
  results: any;
  onReset: () => void;
}

export default function Results({ results, onReset }: ResultsProps) {
  const matchScore = results?.match_result?.score || 0;
  const atsScore = results?.ats_result?.score || 0;
  const overallScore = results?.overall_score || 0;

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBg = (score: number) => {
    if (score >= 80) return 'bg-green-100';
    if (score >= 60) return 'bg-yellow-100';
    return 'bg-red-100';
  };

  return (
    <div className="space-y-6">
      {/* Header with Reset Button */}
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-bold text-navy-900">📊 Analysis Results</h2>
        <button
          onClick={onReset}
          className="px-6 py-2 bg-navy-600 hover:bg-navy-700 text-white rounded-lg font-medium transition"
        >
          ← New Analysis
        </button>
      </div>

      {/* Overall Score */}
      <div className="bg-gradient-to-r from-primary-500 to-primary-600 rounded-lg p-8 text-white shadow-lg">
        <h3 className="text-xl font-semibold mb-2">Overall Score</h3>
        <div className="flex items-end gap-2">
          <span className="text-6xl font-bold">{overallScore}%</span>
          <span className="text-2xl pb-2">/100</span>
        </div>
        <p className="mt-2 text-primary-100">
          {overallScore >= 80 ? 'Excellent! Your resume is well-optimized.' :
           overallScore >= 60 ? 'Good! A few improvements will help.' :
           'Needs work. Follow the suggestions below.'}
        </p>
      </div>

      {/* Score Cards */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* ATS Compatibility Score */}
        <div className="bg-white rounded-lg shadow-lg p-6 border border-navy-100">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-semibold text-navy-900">🤖 ATS Compatibility</h3>
            <span className={`text-3xl font-bold ${getScoreColor(atsScore)}`}>
              {atsScore}%
            </span>
          </div>
          
          <div className="w-full bg-navy-200 rounded-full h-3 mb-4">
            <div
              className={`h-3 rounded-full transition-all ${
                atsScore >= 80 ? 'bg-green-500' :
                atsScore >= 60 ? 'bg-yellow-500' : 'bg-red-500'
              }`}
              style={{ width: `${atsScore}%` }}
            ></div>
          </div>

          <p className="text-sm text-navy-600 mb-3">
            {results?.ats_result?.compatibility || 'Good'}
          </p>

          {results?.ats_result?.issues?.length > 0 && (
            <div>
              <h4 className="font-semibold text-navy-900 mb-2">Issues Found:</h4>
              <div className="space-y-2">
                {results.ats_result.issues.slice(0, 3).map((issue: any, index: number) => (
                  <div key={index} className={`p-3 rounded ${getScoreBg(atsScore)}`}>
                    <p className="text-sm font-medium text-navy-900">{issue.message}</p>
                    <p className="text-xs text-navy-600 mt-1">{issue.fix}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Keyword Match Score */}
        <div className="bg-white rounded-lg shadow-lg p-6 border border-navy-100">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-semibold text-navy-900">🔑 Keyword Match</h3>
            <span className={`text-3xl font-bold ${getScoreColor(matchScore)}`}>
              {matchScore}%
            </span>
          </div>
          
          <div className="w-full bg-navy-200 rounded-full h-3 mb-4">
            <div
              className={`h-3 rounded-full transition-all ${
                matchScore >= 80 ? 'bg-green-500' :
                matchScore >= 60 ? 'bg-yellow-500' : 'bg-red-500'
              }`}
              style={{ width: `${matchScore}%` }}
            ></div>
          </div>

          <p className="text-sm text-navy-600 mb-3">
            {results?.match_result?.matched_keywords || 0} of {results?.match_result?.total_jd_keywords || 0} keywords matched
          </p>

          {results?.match_result?.found_keywords?.length > 0 && (
            <div className="mb-3">
              <h4 className="font-semibold text-navy-900 mb-2">Found Keywords:</h4>
              <div className="flex flex-wrap gap-2">
                {results.match_result.found_keywords.slice(0, 8).map((keyword: string, index: number) => (
                  <span key={index} className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-xs font-medium">
                    ✓ {keyword}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Missing Keywords */}
      {results?.match_result?.missing_keywords?.length > 0 && (
        <div className="bg-white rounded-lg shadow-lg p-6 border border-navy-100">
          <h3 className="text-xl font-semibold text-navy-900 mb-4">⚠️ Missing Keywords</h3>
          <div className="flex flex-wrap gap-2">
            {results.match_result.missing_keywords.map((keyword: string, index: number) => (
              <span key={index} className="px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm font-medium">
                ✗ {keyword}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Optimization Suggestions */}
      {results?.optimization?.priority_fixes?.length > 0 && (
        <div className="bg-white rounded-lg shadow-lg p-6 border border-navy-100">
          <h3 className="text-xl font-semibold text-navy-900 mb-4">💡 Priority Fixes</h3>
          <div className="space-y-3">
            {results.optimization.priority_fixes.map((fix: any, index: number) => (
              <div key={index} className="flex gap-4 p-4 bg-navy-50 rounded-lg">
                <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-white font-bold ${
                  fix.priority === 1 ? 'bg-red-500' : 'bg-yellow-500'
                }`}>
                  {fix.priority}
                </div>
                <div className="flex-1">
                  <p className="font-semibold text-navy-900">{fix.issue}</p>
                  <p className="text-sm text-navy-600 mt-1">{fix.fix}</p>
                  <span className="text-xs text-navy-500 mt-1 inline-block">{fix.category}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Grammar & Style */}
      {results?.grammar_result && (
        <div className="bg-white rounded-lg shadow-lg p-6 border border-navy-100">
          <h3 className="text-xl font-semibold text-navy-900 mb-4">📝 Grammar & Style</h3>
          <div className="grid md:grid-cols-3 gap-4 mb-4">
            <div className="p-4 bg-navy-50 rounded-lg">
              <p className="text-sm text-navy-600">Total Issues</p>
              <p className="text-2xl font-bold text-navy-900">{results.grammar_result.total_issues || 0}</p>
            </div>
            <div className="p-4 bg-navy-50 rounded-lg">
              <p className="text-sm text-navy-600">Readability Score</p>
              <p className="text-2xl font-bold text-navy-900">{results.grammar_result.readability_score || 0}</p>
            </div>
            <div className="p-4 bg-navy-50 rounded-lg">
              <p className="text-sm text-navy-600">Action Verbs</p>
              <p className="text-2xl font-bold text-navy-900">{results.grammar_result.action_verb_count || 0}</p>
            </div>
          </div>
          
          {results.grammar_result.issues?.length > 0 && (
            <div className="space-y-2">
              {results.grammar_result.issues.slice(0, 5).map((issue: any, index: number) => (
                <div key={index} className="p-3 bg-yellow-50 rounded">
                  <p className="text-sm font-medium text-navy-900">{issue.message}</p>
                  <p className="text-xs text-navy-600 mt-1">{issue.suggestion}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Keyword Placement Suggestions */}
      {results?.optimization?.keyword_placement?.length > 0 && (
        <div className="bg-white rounded-lg shadow-lg p-6 border border-navy-100">
          <h3 className="text-xl font-semibold text-navy-900 mb-4">📍 Where to Add Keywords</h3>
          <div className="space-y-4">
            {results.optimization.keyword_placement.slice(0, 5).map((item: any, index: number) => (
              <div key={index} className="border-l-4 border-primary-500 pl-4">
                <p className="font-semibold text-navy-900">Keyword: {item.keyword}</p>
                {item.placements?.map((placement: any, pIndex: number) => (
                  <div key={pIndex} className="mt-2">
                    <p className="text-sm text-navy-700">→ {placement.section}: {placement.suggestion}</p>
                    <p className="text-xs text-navy-500 mt-1 font-mono bg-navy-50 p-2 rounded">
                      {placement.example}
                    </p>
                  </div>
                ))}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
