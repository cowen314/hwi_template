import React from 'react'
import logo from './logo.svg'
import './App.css'
import HomeTab from './components/HomeTab'
import io from 'socket.io-client'
import Dashboard from './dashboard/Dashboard'

function App () {
  const socket = io.connect('http://localhost:5001')
  return (
    <div>
      <div>
        <Dashboard></Dashboard>
        {/* <HomeTab socket={socket} name="Test"/> */}
      </div>
    </div>
  )
}

export default App
