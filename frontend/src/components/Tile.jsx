import React from 'react'
import Tree from './Tree'
import './Tile.css'

function Tile({ tile, tileSize, onTreeCut }) {
  const { x, y, tile_type, tile_image_url, trees } = tile

  const getTileColor = (type) => {
    const colors = {
      grass: '#7cb342',    // Green
      dirt: '#8d6e63',     // Brown
      water: '#42a5f5'     // Blue
    }
    return colors[type] || '#666'
  }

  return (
    <div 
      className="tile"
      data-tile-type={tile_type}
      style={{
        width: `${tileSize}px`,
        height: `${tileSize}px`,
        gridColumn: x + 1,
        gridRow: y + 1,
        backgroundColor: getTileColor(tile_type),
        backgroundImage: tile_image_url ? `url(${tile_image_url})` : undefined,
        backgroundSize: 'cover'
      }}
    >
      {/* Render trees on top of tile */}
      {trees && trees.map(tree => (
        <Tree
          key={tree.id}
          tree={tree}
          tileSize={tileSize}
          onCut={() => onTreeCut(x, y, tree.id)}
        />
      ))}
      
      {/* Debug coordinates (optional) */}
      <span className="tile-coords">{x},{y}</span>
    </div>
  )
}

export default Tile

