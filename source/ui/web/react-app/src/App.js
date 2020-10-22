import React from 'react'
import logo from './logo.svg'
import './App.css'
import HomeTab from './components/HomeTab'
import io from 'socket.io-client'
import Dashboard from './dashboard/Dashboard'
import CompositionApproach from './components/DataPipeline'
import { RechartLineChartExample, RechartScatterExample } from './components/RechartExample'

function App () {
  const socket = io.connect('http://localhost:5001')
  return (
    <div>
      <div>
        {/* <Dashboard socket={socket} name="test key"/> */}
        {/* <Dashboard name="test string" /> */}
        {/* <HomeTab socket={socket} name="Test"/> */}
        {/* <CompositionApproach /> */}
        {/* <RechartLineChartExample /> */}
        <RechartScatterExample />
      </div>
    </div>
  )
}

export default App
