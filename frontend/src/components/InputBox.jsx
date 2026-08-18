import React, { useState } from 'react';
import './InputBox.css';

function InputBox({ onSubmit, loading }) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim() && !loading) {
      onSubmit(query);
    }
  };

  const examples = [
    "I'm going to Bangalore, let's plan my trip",
    "What's the temperature in Paris?",
    "I'm visiting Tokyo, what are the places I can visit and what's the weather?"
  ];

  return (
    <div className="input-box">
      <form onSubmit={handleSubmit}>
        <div className="input-wrapper">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="e.g., I'm going to Bangalore, let's plan my trip"
            disabled={loading}
            className="input-field"
          />
          <button 
            type="submit" 
            disabled={loading || !query.trim()}
            className="submit-button"
          >
            {loading ? '...' : '→'}
          </button>
        </div>
      </form>
      
      <div className="examples">
        <p className="examples-title">Try these examples:</p>
        {examples.map((example, index) => (
          <button
            key={index}
            onClick={() => setQuery(example)}
            className="example-button"
            disabled={loading}
          >
            {example}
          </button>
        ))}
      </div>
    </div>
  );
}

export default InputBox;
