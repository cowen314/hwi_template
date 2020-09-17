Ok, so how could we build web front ends quickly?

How do front end tasks break down by time? 

* Build HTML
* Add interactivity to HTML components (JS)
* Style HTML components (CSS)
* Add endpoints to controllers
* Synchronize DTOs between controllers and views


### High level

TODO

- build a dependency graph for this whole project, structured by user stories
    - root / end node should be something along the lines of "a framework to allow the rapid development of cross platform scientific (data collection and analysis, hardware control, etc) applications"

### Resuable front end components

- Use React

### Backend-frontend runtime data synchronization

- as a front end developer, I would like to refer to pieces of data by name (this name could be called a "tag")
    - when constructing a resuable component, I could pass in the strings that indicate the tags that I'm interested in
    - when components are re-rendered, the latest value of those tags should be used
    - components should only re-render if some of their constituent tag value has changed. Max re-render delay should be ~200ms.
    - there also needs to be a way to handle streaming data (e.g. for plotting)
        - maybe there's some periodic (~200ms) redraw for streamed data... idk
- as a back end developer, I want a "special" (by "special" I just mean that I want it to support streams) CVT that I can read and write values to
    - this CVT would be synchronized with the tag system on the front end
        - e.g. if some back end entity posts to a tag on the CVT, all components on the front end that reference that tag would be updated within ~200ms
        - could a state management framework like Redux help with something like this?

     
Implementation thoughts: 

- So... I think SocketIO, React, and Redux may be able to accomplish this nicely
- server could blast changed (key, value) pairs out every ~200ms
- every time a new message came in from the server, the changed keys could be fed to (Redux) reducer
- the reducer would update the state of the front end, and I think.... the React bindings should re-render all changed components
    - need to figure out how to trigger re-renders on state updates
- Facebook's https://github.com/facebook/create-react-app seems helpful
- Will this work for things that are updated on the front end? What would push front end inputs to the back end?
    - if we can assume that front end input will be event driven, then we can share the probably call a reducer that updates the CVT and pushes the changed data down to the back end CVT

TODO

- Get the redux counter example working 


Redux

- reducers : functions that take an action and the old state and return a new (updated) state
- actions : things that define how the state should be modified

React + Redux

- The entire React app is wrapped by a provider object, which provides the Redux store to the React app
- each React component is run through a Redux function that wraps the React component (reactComponent) => reactComponent
    - there is a standard Redux function collect() that takes two functions as parameters (both are optional)
        - the first parameter/function define how store data is mapped to specific component properties
        - the second parameter/function is confusing and i'll come back to it
    - collect() returns another function which can be used to wrap React components

tutorial notes:

- there are three react components
    - one to create new TODOs, one for TODO items, one to change visibility settings, and one to store a list of TODOs
- the state
    - the todos
    - visibility
    -  
- the actions
    - create a new todo
    - change vis
    - 

questions/thoughts:

- how are events handled?
    - see controlled component section of the React tutorial
    - seems like an action is 'dispatched' ('dispatch' seems to be the standard Redux terminology)
    - an action is somehow routed to a reducer, which updates the state
    - somehow, component properties are mapped to the state of the 


### Backend-frontend datatype synchronization