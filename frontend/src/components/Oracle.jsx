import React, { useState } from 'react'
import './Oracle.css'

function Oracle({ position, tileSize }) {
  const [hover, setHover] = useState(false)

  if (!position) return null

  const oracleSize = tileSize * 0.8 // Oracle is 80% of tile size

  return (
    <div
      className={`oracle ${hover ? 'oracle-hover' : ''}`}
      style={{
        position: 'absolute',
        left: `${position.x * tileSize}px`,
        top: `${position.y * tileSize}px`,
        width: `${tileSize}px`,
        height: `${tileSize}px`,
        zIndex: 100,
        cursor: 'pointer',
        transition: 'all 0.3s ease',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      title="🧙‍♂️ Oracle - The Village Decision Maker"
    >
      <img 
        src="/oracle.png"
        alt="Oracle"
        style={{
          width: `${oracleSize}px`,
          height: `${oracleSize}px`,
          imageRendering: 'pixelated',
          pointerEvents: 'none',
          filter: 'drop-shadow(2px 2px 4px rgba(138, 43, 226, 0.6))'
        }}
        onError={(e) => {
          // Fallback if oracle.png doesn't exist
          e.target.style.display = 'none'
          e.target.parentElement.innerHTML = '<div style="font-size: 48px; text-align: center; line-height: 1;">🧙‍♂️</div>'
        }}
      />
      
      {hover && (
        <div className="oracle-tooltip">
          🧙‍♂️ Village Oracle
        </div>
      )}
    </div>
  )
}

export default Oracle

