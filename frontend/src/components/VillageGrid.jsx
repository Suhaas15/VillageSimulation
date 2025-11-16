import React, { useState, useEffect, useRef, useCallback } from 'react'
import axios from 'axios'
import Tile from './Tile'
import Oracle from './Oracle'
import Builder from './Builder'
import LoadingScreen from './LoadingScreen'
import ActivityLog from './ActivityLog'
import './VillageGrid.css'

const TILE_SIZE = 100 // pixels (100x100 for 10x10 grid)
const API_URL = 'http://localhost:5001/api'

function VillageGrid({ gridSize, onResourcesUpdate }) {
  const [tiles, setTiles] = useState([])
  const [loading, setLoading] = useState(true)
  const [oraclePosition, setOraclePosition] = useState(null)
  const [builders, setBuilders] = useState([])
  const [selectedBuilder, setSelectedBuilder] = useState(null)
  const [activityLogs, setActivityLogs] = useState([])
  
  // Asset generation states
  const [generatingAssets, setGeneratingAssets] = useState(true)
  const [assetProgress, setAssetProgress] = useState(0)
  const [assetStatus, setAssetStatus] = useState('Initializing...')
  const [generatedAssets, setGeneratedAssets] = useState(null)
  const hasLoadedRef = useRef(false)
  
  // Add log entry helper
  const addLog = useCallback((type, message, details = null) => {
    const newLog = {
      type,
      message,
      details,
      timestamp: Date.now()
    }
    setActivityLogs(prev => [...prev, newLog])
  }, [])

  // Log builder action helper
  const logBuilderAction = useCallback((agentId, result) => {
    const action = result.action
    
    if (action === 'cut') {
      const woodGained = result.wood_gained || 0
      const pos = result.position || {}
      addLog('tree_cut', `${agentId} cut tree`, `Gained ${woodGained} wood at (${pos.x}, ${pos.y})`)
      if (woodGained > 0) {
        addLog('resource', `+${woodGained} wood`, `Total resources updated`)
      }
    } else if (action === 'walk') {
      const to = result.to || {}
      addLog('move', `${agentId} moved`, `Walked to (${to.x}, ${to.y})`)
    } else if (action === 'build') {
      const buildingType = result.building_type || 'structure'
      const pos = result.position || {}
      addLog('build', `${agentId} built ${buildingType}`, `Constructed at (${pos.x}, ${pos.y})`)
    } else if (action === 'talk') {
      const msg = result.message || ''
      addLog('talk', `${agentId} says:`, msg)
    }
  }, [addLog])

  // Define functions before useEffect hooks
  const fetchBuilders = useCallback(async () => {
    try {
      const response = await axios.get(`${API_URL}/builder/list`)
      if (response.data.success) {
        setBuilders(response.data.builders)
      }
    } catch (error) {
      console.error('Error fetching builders:', error)
    }
  }, [])

  const fetchGridData = useCallback(async () => {
    try {
      console.log('📡 Fetching grid data...')
      setLoading(true)
      const response = await axios.get(`${API_URL}/grid`)
      console.log('✅ Grid data received:', response.data)
      
      // Apply generated assets to tiles
      let tilesData = response.data.tiles
      if (generatedAssets) {
        console.log('🎨 Applying generated assets to tiles...')
        tilesData = tilesData.map(tile => ({
          ...tile,
          tile_image_url: tile.tile_type === 'grass' && generatedAssets.tiles?.grass 
            ? generatedAssets.tiles.grass 
            : tile.tile_image_url,
          trees: tile.trees?.map(tree => ({
            ...tree,
            image_url: generatedAssets.trees?.[0] || tree.image_url
          }))
        }))
        console.log('✅ Assets applied to tiles')
      }
      
      setTiles(tilesData)
      setOraclePosition(response.data.oracle_position)
      onResourcesUpdate(response.data.resources)
      setLoading(false)
      console.log('✅ Grid loaded successfully')
      if (response.data.oracle_position) {
        console.log(`🧙‍♂️ Oracle at (${response.data.oracle_position.x}, ${response.data.oracle_position.y})`)
      }
    } catch (error) {
      console.error('❌ Error fetching grid:', error)
      setLoading(false)
    }
  }, [onResourcesUpdate, generatedAssets])

  const generateAssets = useCallback(async () => {
    try {
      console.log('🎨 Starting asset generation...')
      setAssetStatus('🎨 Starting AI image generation...')
      setAssetProgress(5)

      // Start the API call
      const apiCall = axios.post(`${API_URL}/assets/generate`)

      // Simplified progress: 1 pine tree + 1 grass tile (~30 seconds total)
      const progressSteps = [
        { delay: 3000, progress: 20, status: '🌲 Generating pine tree image...' },
        { delay: 10000, progress: 50, status: '🎨 Removing background from pine tree...' },
        { delay: 12000, progress: 75, status: '🟩 Generating grass tile...' },
        { delay: 8000, progress: 95, status: '⏳ Finalizing assets...' },
      ]

      for (const step of progressSteps) {
        await new Promise(resolve => setTimeout(resolve, step.delay))
        setAssetProgress(step.progress)
        setAssetStatus(step.status)
      }

      // Wait for API response
      const response = await apiCall
      console.log('✅ Asset generation response:', response.data)

      if (response.data.success) {
        setAssetStatus('✅ Assets ready!')
        setAssetProgress(100)
        
        console.log('🎨 Generated assets:', response.data.assets)
        console.log('   - Pine tree URL:', response.data.assets.trees?.[0])
        console.log('   - Grass tile URL:', response.data.assets.tiles?.grass)
        setGeneratedAssets(response.data.assets)
        console.log('✅ Assets stored, transitioning...')
        
        // Wait a moment before transitioning
        await new Promise(resolve => setTimeout(resolve, 1000))
        console.log('✅ Setting generatingAssets to false')
        setGeneratingAssets(false)
      } else {
        throw new Error('Asset generation failed')
      }
    } catch (err) {
      console.error('❌ Error generating assets:', err)
      setAssetStatus('⚠️ Using placeholder assets...')
      setAssetProgress(100)
      
      // Still proceed with placeholders
      await new Promise(resolve => setTimeout(resolve, 1000))
      console.log('⚠️ Proceeding with placeholders')
      setGeneratingAssets(false)
    }
  }, [])

  // Generate assets first, then fetch grid data
  useEffect(() => {
    generateAssets()
  }, [generateAssets])

  useEffect(() => {
    console.log('📊 State check - generatingAssets:', generatingAssets, 'hasLoaded:', hasLoadedRef.current)
    if (!generatingAssets && !hasLoadedRef.current) {
      console.log('✅ Asset generation complete, fetching grid...')
      hasLoadedRef.current = true
      fetchGridData()
      fetchBuilders() // Also fetch builders on load
    }
  }, [generatingAssets, fetchGridData, fetchBuilders])

  const handleTreeCut = async (x, y, treeId) => {
    try {
      const response = await axios.post(`${API_URL}/tree/cut`, {
        x, y, tree_id: treeId
      })
      
      if (response.data.success) {
        // Update local state
        setTiles(prevTiles => 
          prevTiles.map(tile => {
            if (tile.x === x && tile.y === y) {
              return {
                ...tile,
                trees: tile.trees.map(tree => 
                  tree.id === treeId ? { ...tree, cut: true } : tree
                )
              }
            }
            return tile
          })
        )
        
        // Update resources
        onResourcesUpdate(response.data.total_resources)
        
        // Refresh builders in case one cut the tree
        fetchBuilders()
      }
    } catch (error) {
      console.error('Error cutting tree:', error)
    }
  }

  const handleBuilderClick = (builder) => {
    setSelectedBuilder(builder)
  }

  const createBuilder = async () => {
    try {
      const response = await axios.post(`${API_URL}/builder/create`, {}, {
        headers: {
          'Content-Type': 'application/json'
        }
      })
      if (response.data.success) {
        const agentId = response.data.agent_id
        const pos = response.data.state.position
        console.log('✅ Builder created:', agentId)
        addLog('system', `Builder ${agentId} created`, `Spawned at (${pos.x}, ${pos.y}) near Oracle`)
        fetchBuilders()
      }
    } catch (error) {
      console.error('Error creating builder:', error)
      addLog('system', 'Failed to create builder', error.message)
    }
  }

  const makeBuilderAct = async (agentId) => {
    try {
      const response = await axios.post(`${API_URL}/builder/${agentId}/act`, {}, {
        headers: { 'Content-Type': 'application/json' }
      })
      if (response.data.success) {
        const result = response.data.result
        console.log('✅ Builder action:', result)
        
        // Log the action
        addLog('builder', `${agentId} acted`, 'Builder AI decided action')
        logBuilderAction(agentId, result)
        
        // Wait a bit then refresh to see movement
        setTimeout(() => {
          fetchBuilders()
          fetchGridData()
        }, 100)
        
        // After completing action, consult Oracle for next strategic direction
        setTimeout(async () => {
          addLog('system', `${agentId} consulting Oracle after completing task...`)
          await makeBuilderOracleAct(agentId)
        }, 1500)
      }
    } catch (error) {
      console.error('Error making builder act:', error)
      addLog('builder', `${agentId} action failed`, error.message)
    }
  }

  const makeBuilderOracleAct = async (agentId) => {
    try {
      const response = await axios.post(`${API_URL}/builder/${agentId}/oracle_act`, {}, {
        headers: { 'Content-Type': 'application/json' }
      })
      if (response.data.success) {
        const directive = response.data.oracle_directive
        const actionCmd = response.data.action_command
        const executionResult = response.data.execution_result
        
        console.log('🔮 Oracle directive:', directive)
        console.log('🤖 Action command:', actionCmd)
        console.log('✅ Execution:', executionResult)
        
        // Log Oracle directive
        addLog('oracle', 'Oracle commanded:', directive)
        
        // Log Builder action
        addLog('builder', `${agentId} executing:`, actionCmd)
        
        // Log execution result
        logBuilderAction(agentId, executionResult)
        
        // Wait a bit then refresh to see movement
        setTimeout(() => {
          fetchBuilders()
          fetchGridData()
        }, 100)
      }
    } catch (error) {
      console.error('Error making builder oracle act:', error)
      addLog('oracle', 'Oracle consultation failed', error.message)
    }
  }

  const simulateBuilder = async (agentId, steps = 5) => {
    let pollInterval = null
    try {
      console.log(`⏳ Starting ${steps}-step simulation...`)
      addLog('system', `Starting ${steps}-step Builder AI simulation for ${agentId}`)
      
      // Start polling for updates during simulation
      pollInterval = setInterval(() => {
        fetchBuilders()
        fetchGridData()
      }, 2000) // Refresh every 2 seconds
      
      const response = await axios.post(`${API_URL}/builder/${agentId}/simulate`, { 
        steps, 
        delay: 5 
      }, {
        headers: { 'Content-Type': 'application/json' }
      })
      
      if (response.data.success) {
        console.log(`✅ Builder simulated ${response.data.steps_executed} steps`)
        addLog('system', `✅ Completed ${response.data.steps_executed} Builder AI steps`)
        
        // Parse and log each step's results
        if (response.data.results && Array.isArray(response.data.results)) {
          response.data.results.forEach((stepResult, index) => {
            if (stepResult.result) {
              addLog('builder', `Step ${stepResult.step}: ${agentId} AI action`)
              logBuilderAction(agentId, stepResult.result)
            }
          })
        }
        
        // After completing AI simulation, consult Oracle for next strategic direction
        addLog('system', `${agentId} consulting Oracle after completing tasks...`)
        setTimeout(async () => {
          await makeBuilderOracleAct(agentId)
        }, 1000)
        
        // Final refresh to ensure everything is updated
        setTimeout(() => {
          fetchBuilders()
          fetchGridData()
        }, 500)
      }
    } catch (error) {
      console.error('Error simulating builder:', error)
      addLog('system', `❌ Builder simulation failed`, error.message)
    } finally {
      // Always stop polling
      if (pollInterval) clearInterval(pollInterval)
    }
  }

  const simulateBuilderOracle = async (agentId, steps = 3) => {
    let pollInterval = null
    try {
      console.log(`⏳ Starting ${steps}-step Oracle simulation...`)
      addLog('system', `Starting ${steps}-step Oracle simulation for ${agentId}`)
      
      // Start polling for updates during simulation
      pollInterval = setInterval(() => {
        fetchBuilders()
        fetchGridData()
      }, 2000) // Refresh every 2 seconds
      
      const response = await axios.post(`${API_URL}/builder/${agentId}/oracle_simulate`, { 
        steps, 
        delay: 5 
      }, {
        headers: { 'Content-Type': 'application/json' }
      })
      
      if (response.data.success) {
        console.log(`🔮 Builder Oracle simulated ${response.data.steps_executed} steps`)
        addLog('system', `✅ Completed ${response.data.steps_executed} steps`)
        
        // Parse and log each step's results
        if (response.data.results && Array.isArray(response.data.results)) {
          response.data.results.forEach((stepResult, index) => {
            // Log Oracle directive
            if (stepResult.oracle_directive) {
              addLog('oracle', `Step ${stepResult.step}: Oracle commanded`, stepResult.oracle_directive)
            }
            
            // Log Builder action command
            if (stepResult.action_command) {
              addLog('builder', `Step ${stepResult.step}: ${agentId} executing`, stepResult.action_command)
            }
            
            // Log execution result details
            if (stepResult.execution_result) {
              logBuilderAction(agentId, stepResult.execution_result)
            }
          })
        }
        
        // Final refresh to ensure everything is updated
        setTimeout(() => {
          fetchBuilders()
          fetchGridData()
        }, 500)
      }
    } catch (error) {
      console.error('Error simulating builder oracle:', error)
      addLog('system', `❌ Oracle simulation failed`, error.message)
    } finally {
      // Always stop polling
      if (pollInterval) clearInterval(pollInterval)
    }
  }

  // Show loading screen while generating assets
  if (generatingAssets) {
    return (
      <LoadingScreen 
        progress={assetProgress} 
        status={assetStatus}
      />
    )
  }

  if (loading) {
    return (
      <div className="grid-loading">
        <div className="spinner"></div>
        <p>Loading village...</p>
      </div>
    )
  }

  return (
    <div className="village-main-layout">
      {/* CONTROLS CONTAINER - Activity Log + Builder Menu */}
      <div className="controls-container">
        {/* Activity Log */}
        <ActivityLog logs={activityLogs} />
        
        {/* Builder control panel */}
        <div className="builder-control-panel">
          <div className="control-header">
            <h3>🏗️ Builder Controls</h3>
            <button onClick={createBuilder} className="create-builder-btn">
              + Create Builder
            </button>
          </div>
          
          {builders.length === 0 && (
            <div className="no-builders">
              No builders yet. Click "Create Builder" to add one!
            </div>
          )}
          
          {builders.map(builder => (
            <div 
              key={builder.agent_id} 
              className={`builder-card ${selectedBuilder?.agent_id === builder.agent_id ? 'selected' : ''}`}
              onClick={() => handleBuilderClick(builder)}
            >
              <div className="builder-card-header">
                <span className="builder-name">{builder.agent_id}</span>
                <span className="builder-position">({builder.position.x}, {builder.position.y})</span>
              </div>
              <div className="builder-inventory-small">
                <span>🪵 {builder.inventory.wood}</span>
                <span>🪨 {builder.inventory.stone}</span>
                <span>🍎 {builder.inventory.food}</span>
              </div>
              <div className="builder-actions">
                <button 
                  onClick={(e) => { e.stopPropagation(); makeBuilderOracleAct(builder.agent_id); }}
                  className="action-btn oracle-btn"
                  title="Oracle gives directive, Builder AI executes"
                >
                  🔮 Oracle
                </button>
                <button 
                  onClick={(e) => { e.stopPropagation(); simulateBuilderOracle(builder.agent_id, 3); }}
                  className="action-btn oracle-btn"
                  title="Run 3 Oracle-guided actions (5s delay each)"
                >
                  🔮 Run 3
                </button>
              </div>
              <div className="builder-actions" style={{ marginTop: '4px' }}>
                <button 
                  onClick={(e) => { e.stopPropagation(); makeBuilderAct(builder.agent_id); }}
                  className="action-btn"
                  title="Builder AI decides directly"
                >
                  🤖 AI
                </button>
                <button 
                  onClick={(e) => { e.stopPropagation(); simulateBuilder(builder.agent_id, 5); }}
                  className="action-btn"
                  title="Run 5 Builder AI actions (5s delay each)"
                >
                  ▶️ Run 5
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* GRID CONTAINER - Game Grid Only */}
      <div className="grid-container">
        <div 
          className="village-grid"
          style={{
            width: `${gridSize * TILE_SIZE}px`,
            height: `${gridSize * TILE_SIZE}px`
          }}
        >
          {tiles.map(tile => (
            <Tile
              key={`${tile.x}-${tile.y}`}
              tile={tile}
              tileSize={TILE_SIZE}
              onTreeCut={handleTreeCut}
            />
          ))}
          
          {/* Render Oracle character */}
          <Oracle 
            position={oraclePosition}
            tileSize={TILE_SIZE}
          />
          
          {/* Render Builders */}
          {builders.map(builder => (
            <Builder
              key={builder.agent_id}
              builder={builder}
              gridSize={gridSize}
              tileSize={TILE_SIZE}
              onClick={handleBuilderClick}
            />
          ))}
        </div>
      </div>
    </div>
  )
}

export default VillageGrid

