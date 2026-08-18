import React, { useState } from 'react';
import InputBox from './components/InputBox';
import ResultBox from './components/ResultBox';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleQuery = async (query) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch(`${API_URL}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      const data = await response.json();

      if (data.success) {
        setResult(data);
      } else {
        setError(data.message || 'An error occurred');
      }
    } catch (err) {
      setError('Failed to connect to the server. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="container">
        <h1 className="title">🌍 Tourism AI</h1>
        <p className="subtitle">Plan your perfect trip with AI-powered recommendations</p>
        
        <InputBox onSubmit={handleQuery} loading={loading} />
        
        {error && (
          <div className="error-box">
            <p>{error}</p>
          </div>
        )}
        
        {result && <ResultBox result={result} />}
      </div>
    </div>
  );
}

export default App;
