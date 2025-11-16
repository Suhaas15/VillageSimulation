import React, { useState } from 'react'
import './Builder.css'

const Builder = ({ builder, gridSize, tileSize, onClick }) => {
  const [hover, setHover] = useState(false)

  if (!builder || !builder.position) return null

  const { x, y } = builder.position
  const { inventory, agent_id } = builder

  // Calculate pixel position
  const left = x * tileSize
  const top = y * tileSize
  const spriteSize = tileSize * 0.8 // Builder sprite is 80% of tile

  return (
    <div
      className={`builder ${hover ? 'builder-hover' : ''}`}
      style={{
        position: 'absolute',
        left: `${left}px`,
        top: `${top}px`,
        width: `${tileSize}px`,
        height: `${tileSize}px`,
        zIndex: 100,
        cursor: 'pointer',
        transition: 'left 0.5s ease-in-out, top 0.5s ease-in-out',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }}
      onClick={() => onClick && onClick(builder)}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      title={`Builder ${agent_id} - Click for actions`}
    >
      {/* Builder sprite image */}
      <img 
        src="/builder.png" 
        alt="Builder"
        className="builder-sprite-img"
        style={{
          width: `${spriteSize}px`,
          height: `${spriteSize}px`,
          imageRendering: 'pixelated',
          objectFit: 'contain'
        }}
      />

      {/* Inventory badge */}
      {(inventory.wood > 0 || inventory.stone > 0) && (
        <div className="builder-inventory-badge">
          {inventory.wood > 0 && <span className="wood-badge">🪵 {inventory.wood}</span>}
          {inventory.stone > 0 && <span className="stone-badge">🪨 {inventory.stone}</span>}
        </div>
      )}

      {/* Info tooltip on hover */}
      {hover && (
        <div className="builder-tooltip">
          <div className="tooltip-title">{agent_id}</div>
          <div className="tooltip-position">Position: ({x}, {y})</div>
          <div className="tooltip-inventory">
            <div>🪵 Wood: {inventory.wood}</div>
            <div>🪨 Stone: {inventory.stone}</div>
            <div>🍎 Food: {inventory.food}</div>
          </div>
          <div className="tooltip-hint">Click to control</div>
        </div>
      )}
    </div>
  )
}

export default Builder

