import React, { Component, useState, useEffect } from 'react';
import io from 'socket.io-client';

class HomeTab extends React.Component {
    constructor(props) {
        super(props);
        // this.state = {date: new Date(), count: 0};
    }

    

    render(props) { 
        return <>
            <div>
                <DateAndCounter />
            </div>
            <div>
                <ValueTable />
                <AAdder />
                <SigleValue socket={io("127.0.0.1:5001")}/> //
            </div>

        </>;
    };
};


class ValueTable extends React.Component {
    constructor(props) {
        super(props);
    }

    // How do I generate HTML programatically?
    // Eventually, populate the table with whatever initial variables and values are passed in to the constructor
        // on ComponentDidMount() of the HomeTab component, fetch all available keys  

    render(props) {
        return <>
            <table>
                <thead>
                    <tr>
                        <td>Name</td>
                        <td>Value</td>
                    </tr>
                </thead>
            </table>
        </>;
    }
}


function AAdder(){
    const [text, setText] = useState("initial");  // returns a state "thing" (variable?) and a function to set that thing 
    return <>
    <button onClick={() => setText(text+"a")}>Test</button>
    <p>{text}</p>
    </>
}


function SingleValue(props) {
    const [value, setValue] = useState(-1);
    useEffect({
        // a function that subscribes this component to updates pushed over the web socket
        props.socket.connect("");
    })
    return <>
        <p>{value}</p>
    </>
}


class DateAndCounter extends React.Component {
    constructor(props) {
        super(props);
        this.state = {date: new Date(), count: 0};

        // be sure to bind callbacks to the class! (this lets you refer to them as 'this.<method_name>')
        this.handleButtonPress = this.handleButtonPress.bind(this);
    }

    handleButtonPress() {
        this.setState(state => ({
            date : state.date,
            count : ++state.count
        }));
    }
    
    render(props) { 
        return <>
        <p>
            The date is {this.state.date.toDateString()} <br/>
            The button has been pressed {this.state.count} times
        </p>
        <button onClick={this.handleButtonPress}>Press here</button>
        </>;
    };
}

export default HomeTab;