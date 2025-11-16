import React, { useEffect, useRef } from 'react'
import './ActivityLog.css'

const ActivityLog = ({ logs }) => {
  const logEndRef = useRef(null)

  useEffect(() => {
    // Auto-scroll to bottom when new logs added
    logEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [logs])

  const getLogIcon = (type) => {
    const icons = {
      'oracle': '🔮',
      'builder': '🏗️',
      'tree_cut': '🪓',
      'resource': '📦',
      'move': '🚶',
      'build': '🏠',
      'talk': '💬',
      'system': 'ℹ️'
    }
    return icons[type] || '•'
  }

  const getLogClass = (type) => {
    return `log-entry log-${type}`
  }

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp)
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit', 
      second: '2-digit' 
    })
  }

  return (
    <div className="activity-log">
      <div className="activity-log-header">
        <h3>📜 Activity Log</h3>
        <span className="log-count">{logs.length} events</span>
      </div>
      
      <div className="activity-log-content">
        {logs.length === 0 ? (
          <div className="log-empty">
            <p>No activity yet...</p>
            <p className="log-hint">Actions will appear here as they happen</p>
          </div>
        ) : (
          logs.map((log, index) => (
            <div key={index} className={getLogClass(log.type)}>
              <span className="log-icon">{getLogIcon(log.type)}</span>
              <div className="log-details">
                <div className="log-message">{log.message}</div>
                {log.details && (
                  <div className="log-subtext">{log.details}</div>
                )}
                <div className="log-timestamp">{formatTimestamp(log.timestamp)}</div>
              </div>
            </div>
          ))
        )}
        <div ref={logEndRef} />
      </div>
      
      <div className="activity-log-footer">
        <button 
          onClick={() => window.location.reload()} 
          className="clear-log-btn"
          title="Refresh page to clear log"
        >
          🔄 Refresh
        </button>
      </div>
    </div>
  )
}

export default ActivityLog

