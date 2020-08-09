import { createStore } from 'redux'

function cvt(state, action) {
    // the action will contain the newly updated keys
    // add changed values to corresponding keys (in CVT) here
    new_state = state;
    for item in action {
        new_state[item.key] = item.value;
    }
    return new_state;
}

let store = createStore(cvt);

store.dispatch({
    "testKeyA": "testvalue",
    "testKeyB": "testvalue"
});

// TODO dispatch action on inbound socket.io message
var socket = io.connect('http://127.0.0.1:5001');
// verify our websocket connection is established
socket.on('connect', function() {
    console.log('Websocket connected!');
    // TODO request full state (HTTP GET) and run full state through cvt()
});