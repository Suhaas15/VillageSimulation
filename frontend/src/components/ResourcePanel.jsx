import React, { useState, useEffect } from 'react'
import './ResourcePanel.css'

function ResourcePanel({ resources }) {
  const [prevResources, setPrevResources] = useState(resources)
  const [animating, setAnimating] = useState({ wood: false, stone: false, food: false })

  useEffect(() => {
    // Detect changes and trigger animations
    const newAnimating = {
      wood: resources.wood !== prevResources.wood,
      stone: resources.stone !== prevResources.stone,
      food: resources.food !== prevResources.food
    }
    
    setAnimating(newAnimating)
    
    // Reset animations after delay
    const timer = setTimeout(() => {
      setAnimating({ wood: false, stone: false, food: false })
    }, 600)
    
    setPrevResources(resources)
    
    return () => clearTimeout(timer)
  }, [resources, prevResources])

  return (
    <div className="resource-panel">
      <div className={`resource-item ${animating.wood ? 'resource-increased' : ''}`}>
        <span className="resource-icon">🪵</span>
        <span className="resource-label">Wood</span>
        <span className="resource-value">{resources.wood}</span>
        {animating.wood && resources.wood > prevResources.wood && (
          <span className="resource-change">+{resources.wood - prevResources.wood}</span>
        )}
      </div>
      
      <div className={`resource-item ${animating.stone ? 'resource-increased' : ''}`}>
        <span className="resource-icon">🪨</span>
        <span className="resource-label">Stone</span>
        <span className="resource-value">{resources.stone}</span>
        {animating.stone && resources.stone > prevResources.stone && (
          <span className="resource-change">+{resources.stone - prevResources.stone}</span>
        )}
      </div>
      
      <div className={`resource-item ${animating.food ? 'resource-increased' : ''}`}>
        <span className="resource-icon">🌾</span>
        <span className="resource-label">Food</span>
        <span className="resource-value">{resources.food}</span>
        {animating.food && resources.food > prevResources.food && (
          <span className="resource-change">+{resources.food - prevResources.food}</span>
        )}
      </div>
    </div>
  )
}

export default ResourcePanel

