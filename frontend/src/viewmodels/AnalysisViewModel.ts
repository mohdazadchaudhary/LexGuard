import { useState } from 'react';

export const useAnalysisViewModel = () => {
  const [text, setText] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const analyzeDocument = async (documentText: string) => {
    if (!documentText.trim()) {
      setError('Please provide text to analyze.');
      return;
    }

    setIsAnalyzing(true);
    setError(null);
    setAnalysisResult(null);

    try {
      // Pointing to the FastAPI backend running locally
      const response = await fetch('http://localhost:8000/api/v1/analysis/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: documentText }),
      });

      if (!response.ok) {
        throw new Error('Failed to analyze document. Server responded with an error.');
      }

      const data = await response.json();
      setAnalysisResult(data.analysis);
    } catch (err: any) {
      setError(err.message || 'An unexpected error occurred during analysis.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const clearAnalysis = () => {
    setText('');
    setAnalysisResult(null);
    setError(null);
  };

  return {
    text,
    setText,
    isAnalyzing,
    analysisResult,
    error,
    analyzeDocument,
    clearAnalysis,
  };
};
