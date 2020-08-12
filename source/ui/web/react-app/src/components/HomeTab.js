import React, { Component } from 'react';

class HomeTab extends React.Component {
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
};

class ValueTable extends React.Component {
    constructor(props) {
        // TODO implement a value table
    }
}

export default HomeTab;