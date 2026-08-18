import React from 'react';
import './ResultBox.css';

function ResultBox({ result }) {
  const formatMessage = (message) => {
    // Split by newlines and format
    const lines = message.split('\n');
    return lines.map((line, index) => {
      if (line.startsWith('-')) {
        return (
          <li key={index} className="attraction-item">
            {line.substring(1).trim()}
          </li>
        );
      }
      return null;
    });
  };

  const getMainText = (message) => {
    const lines = message.split('\n');
    return lines[0];
  };

  const hasAttractions = (message) => {
    return message.includes('\n-');
  };

  return (
    <div className="result-box">
      <div className="result-header">
        <h3>✨ Your Travel Information</h3>
        {result.place && (
          <span className="place-badge">{result.place}</span>
        )}
      </div>
      
      <div className="result-content">
        <p className="main-text">{getMainText(result.message)}</p>
        
        {hasAttractions(result.message) && (
          <ul className="attractions-list">
            {formatMessage(result.message)}
          </ul>
        )}
      </div>
      
      <div className="result-footer">
        <span className="intent-badge">
          {result.intent === 'both' ? '🌤️ Weather + 📍 Places' : 
           result.intent === 'weather' ? '🌤️ Weather Info' : 
           '📍 Places to Visit'}
        </span>
      </div>
    </div>
  );
}

export default ResultBox;
