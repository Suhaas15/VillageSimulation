import React from 'react'
import './LoadingScreen.css'

function LoadingScreen({ progress, status }) {
  return (
    <div className="loading-screen">
      <div className="loading-content">
        <h1 className="loading-title">🌳 The Village Project</h1>
        <p className="loading-subtitle">Generating AI Assets with Freepik</p>
        
        <div className="loading-bar-container">
          <div className="loading-bar" style={{ width: `${progress}%` }}>
            <div className="loading-bar-shine"></div>
          </div>
        </div>
        
        <div className="loading-percentage">{Math.round(progress)}%</div>
        
        <div className="loading-status">
          {status}
        </div>
        
        <div className="loading-info">
          <div className="info-item">
            <span className="info-icon">🌲</span>
            <span>Generating 1 pine tree sprite</span>
          </div>
          <div className="info-item">
            <span className="info-icon">🎨</span>
            <span>Removing background with AI</span>
          </div>
          <div className="info-item">
            <span className="info-icon">🟩</span>
            <span>Creating grass tile texture</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default LoadingScreen

