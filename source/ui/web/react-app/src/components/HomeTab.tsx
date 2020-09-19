/* eslint-disable no-useless-constructor */
import React, { useState, useEffect } from 'react'
import BasicPlotlyGraph from './Graphs'

interface socketType {  // example of a typescript interface
  on: (eventName: string, callback: any) => (any);
  emit: (tag: string, data: any) => void;
}

interface HomeTabProps {  // another example
  socket: socketType;
  name: string;
}

function HomeTab (props: HomeTabProps) {

  return <>
    <div>
      {/* <DateAndCounter /> */}
    </div>
    <div>
      <ValueTable value={5} />
      <AAdder />
      <SingleValue socket={props.socket} tag="fromServer"/>
      <SocketTestButton socket={props.socket}/>
      <ConnectionStatus socket={props.socket}/>
      <BasicPlotlyGraph />
    </div>

  </>
};

function ValueTable (props: {value: number}) {

  // How do I generate HTML programatically?
  // Eventually, populate the table with whatever initial variables and values are passed in to the constructor
  // on ComponentDidMount() of the HomeTab component, fetch all available keys

  return <>
    <table>
      <thead>
        <tr>
          <td>Name</td>
          <td>Value</td>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Example</td> 
          <td>{props.value}</td>
        </tr>
      </tbody>
    </table>
  </>
}

function AAdder () {
  const [text, setText] = useState('initial') // returns a state "thing" (variable?) and a function to set that thing
  return <>
    <button onClick={() => setText(text + 'a')}>Test</button>
    <p>{text}</p>
  </>
}

function SingleValue (props: {socket: socketType, tag: string}) {
  // const value = useNumericValue(props.socket, props.key)
  const [value, setValue] = useState(0)
  // const [renderCount, setRenderCount] = useState(0);
  useEffect(() => {
    // check to see if a connection already exists
    props.socket.on(props.tag, (value: number) => {
      setValue(value);
      // setRenderCount(renderCount+1);  // for some reason, enabling this line causes updates to take longer and longer after evey rerender
    }
    )  // do not name any prop "key"... "key" seems to be reserved
    // maybe return a function to cleanup the connection?
  })

  return <>
    <p>{value}</p>
    {/* <useNumericValue/> */}
    {/* <p>{useNumericValue}</p> */}
  </>
}

// TODO get this working later
function ConnectionStatus(props: {socket: socketType}) {
  const [connected, setConnected] = useState(false)
  useEffect(() => {
    // maybe add some logic to `connected` to the correct state initially
    if ({connected})
      props.socket.on("disconnect", () => setConnected(false));
    else
      props.socket.on("connection", () => setConnected(true));
  })
  const status = {connected} ? "Connected" : "Disconnected";
  // const status = true ? "Connected" : "Disconnected";
  return <>{status}</>
}

function SocketTestButton (props: {socket: socketType}) {
  return <>
    <button onClick={() => props.socket.emit('test', {'data':'test data'})}> Test Socket </button>
  </>
}

// class DateAndCounter extends React.Component {
//   constructor (props: any) {
//     super(props)
//     this.state = { date: new Date(), count: 0 }

//     // be sure to bind callbacks to the class! (this lets you refer to them as 'this.<method_name>')
//     this.handleButtonPress = this.handleButtonPress.bind(this)
//   }

//   handleButtonPress () {
//     this.setState(state: (any) => ({  // : {date: any, count: number}
//       date: state.date,
//       count: ++state.count
//     }))
//   }

//   render () {
//     return <>
//       <p>
//             The date is {this.state.date.toDateString()} <br/>
//             The button has been pressed {this.state.count} times
//       </p>
//       <button onClick={this.handleButtonPress}>Press here</button>
//     </>
//   };
// }

export default HomeTab
