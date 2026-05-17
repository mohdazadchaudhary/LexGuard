import { useState } from 'react';

export const useAnalysisViewModel = () => {
  const [text, setText] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [chatMessages, setChatMessages] = useState<{ sender: 'user' | 'bot'; text: string }[]>([]);
  const [isChatting, setIsChatting] = useState(false);
  const [chatInput, setChatInput] = useState('');

  const analyzeDocument = async () => {
    if (!text.trim() && !file) {
      setError('Please provide text or upload a PDF to analyze.');
      return;
    }

    setIsAnalyzing(true);
    setError(null);
    setAnalysisResult(null);
    setChatMessages([]);

    try {
      let response;
      if (file) {
        // Upload file
        const formData = new FormData();
        formData.append('file', file);
        response = await fetch('http://localhost:8000/api/v1/analysis/upload', {
          method: 'POST',
          body: formData,
        });
      } else {
        // Send text
        response = await fetch('http://localhost:8000/api/v1/analysis/analyze', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ text }),
        });
      }

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to analyze document.');
      }

      const data = await response.json();
      setAnalysisResult(data.analysis);
      if (data.extracted_text) {
        setText(data.extracted_text);
      }
    } catch (err: any) {
      setError(err.message || 'An unexpected error occurred during analysis.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const sendChatMessage = async () => {
    if (!chatInput.trim() || !text.trim()) return;

    const userMsg = chatInput.trim();
    setChatMessages((prev) => [...prev, { sender: 'user', text: userMsg }]);
    setChatInput('');
    setIsChatting(true);

    try {
      const response = await fetch('http://localhost:8000/api/v1/analysis/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text, question: userMsg }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch answer.');
      }

      const data = await response.json();
      setChatMessages((prev) => [...prev, { sender: 'bot', text: data.answer }]);
    } catch (err: any) {
      setChatMessages((prev) => [...prev, { sender: 'bot', text: 'Error: Failed to fetch answer.' }]);
    } finally {
      setIsChatting(false);
    }
  };

  const clearAnalysis = () => {
    setText('');
    setFile(null);
    setAnalysisResult(null);
    setError(null);
    setChatMessages([]);
    setChatInput('');
  };

  return {
    text,
    setText,
    file,
    setFile,
    isAnalyzing,
    analysisResult,
    error,
    chatMessages,
    isChatting,
    chatInput,
    setChatInput,
    analyzeDocument,
    sendChatMessage,
    clearAnalysis,
  };
};
