import React, { useState } from 'react'
import './Tree.css'

function Tree({ tree, tileSize, onCut }) {
  const { id, position, cut, type, image_url } = tree
  const [hover, setHover] = useState(false)

  if (cut) return null // Don't render cut trees

  const handleClick = (e) => {
    e.stopPropagation() // Prevent grid panning
    onCut()
  }

  const treeSize = tileSize * 0.5 // Tree is 50% of tile size (smaller for larger tiles)
  
  // Always use tree.png for now
  const treeImageSrc = '/tree.png'

  return (
    <div
      className={`tree ${hover ? 'tree-hover' : ''}`}
      style={{
        position: 'absolute',
        left: `${position.offset_x * tileSize}px`,
        top: `${position.offset_y * tileSize}px`,
        transform: 'translate(-50%, -50%)',
        cursor: 'pointer',
        zIndex: 10,
        transition: 'transform 0.2s ease',
        width: `${treeSize}px`,
        height: `${treeSize}px`
      }}
      onClick={handleClick}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      title={`${type} tree - Click to cut`}
    >
      <img 
        src={treeImageSrc} 
        alt={`${type} tree`}
        style={{
          width: '100%',
          height: '100%',
          imageRendering: 'pixelated', // Pixelated rendering for tree.png
          pointerEvents: 'none'
        }}
      />
      
      {hover && (
        <div className="tree-tooltip">
          🪓 Cut {type}
        </div>
      )}
    </div>
  )
}

export default Tree

