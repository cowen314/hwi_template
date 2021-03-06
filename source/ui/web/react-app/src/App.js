import React from 'react'
import logo from './logo.svg'
import './App.css'
import HomeTab from './components/HomeTab'
import io from 'socket.io-client'

function App () {
  const socket = io.connect('http://localhost:5001')
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
      <div>
        <HomeTab socket={socket} name="Test"/>
      </div>

    </div>
  )
}

export default App
