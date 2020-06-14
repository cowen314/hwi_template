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