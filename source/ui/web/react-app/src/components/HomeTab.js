/* eslint-disable no-useless-constructor */
import React, { useState, useEffect } from 'react'

class HomeTab extends React.Component {
  constructor (props) {
    super(props)
  }

  render () {
    return <>
      <div>
        <DateAndCounter />
      </div>
      <div>
        <ValueTable />
        <AAdder />
        <SingleValue socket={this.props.socket} tag="fromServer"/>
        <SocketTestButton socket={this.props.socket}/>
        <ConnectionStatus socket={this.props.socket}/>
      </div>

    </>
  };
};

class ValueTable extends React.Component {
  constructor (props) {
    super(props)
  }

  // How do I generate HTML programatically?
  // Eventually, populate the table with whatever initial variables and values are passed in to the constructor
  // on ComponentDidMount() of the HomeTab component, fetch all available keys

  render (props) {
    return <>
      <table>
        <thead>
          <tr>
            <td>Name</td>
            <td>Value</td>
          </tr>
        </thead>
      </table>
    </>
  }
}

function AAdder () {
  const [text, setText] = useState('initial') // returns a state "thing" (variable?) and a function to set that thing
  return <>
    <button onClick={() => setText(text + 'a')}>Test</button>
    <p>{text}</p>
  </>
}

function SingleValue (props) {
  // const value = useNumericValue(props.socket, props.key)
  const [value, setValue] = useState(0)
  useEffect(() => {
    // check to see if a connection already exists
    props.socket.on(props.tag, (value) => setValue(value))  // do not name any prop "key"... "key" seems to be reserved
    // maybe return a function to cleanup the connection?
  })
  return <>
    <p>{value}</p>
    {/* <useNumericValue/> */}
    {/* <p>{useNumericValue}</p> */}
  </>
}

function ConnectionStatus(props) {
  const [connected, setConnected] = useState(false)
  useEffect(() => {
    if ({connected})
      props.socket.on("disconnected", () => setConnected(false));
    else
      props.socket.on("connected", () => setConnected(true));
  })
  // const status = {connected} ? "Connected" : "Disconnected";
  const status = true ? "Connected" : "Disconnected";
  return <>{status}</>
}

function SocketTestButton (props) {
  return <>
    <button onClick={() => props.socket.emit('test', {'data':'test data'})}> Test Socket </button>
  </>
}

class DateAndCounter extends React.Component {
  constructor (props) {
    super(props)
    this.state = { date: new Date(), count: 0 }

    // be sure to bind callbacks to the class! (this lets you refer to them as 'this.<method_name>')
    this.handleButtonPress = this.handleButtonPress.bind(this)
  }

  handleButtonPress () {
    this.setState(state => ({
      date: state.date,
      count: ++state.count
    }))
  }

  render (props) {
    return <>
      <p>
            The date is {this.state.date.toDateString()} <br/>
            The button has been pressed {this.state.count} times
      </p>
      <button onClick={this.handleButtonPress}>Press here</button>
    </>
  };
}

export default HomeTab
