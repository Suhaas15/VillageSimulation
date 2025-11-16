import React, { useState, useEffect } from 'react'
import VillageGrid from './components/VillageGrid'
import ResourcePanel from './components/ResourcePanel'
import './App.css'

function App() {
  const [resources, setResources] = useState({ wood: 0, stone: 0, food: 0 })
  const [gridSize, setGridSize] = useState(10)

  const updateResources = (newResources) => {
    setResources(newResources)
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🌳 The Village Project</h1>
        <p>Click trees to gather resources</p>
      </header>
      
      <ResourcePanel resources={resources} />
      
      <VillageGrid 
        gridSize={gridSize}
        onResourcesUpdate={updateResources}
      />
    </div>
  )
}

export default App

