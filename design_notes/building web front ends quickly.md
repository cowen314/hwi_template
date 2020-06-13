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

- keep a web socket open, and use it to push updates from the back end to the front end
    - not exactly sure how to do this while also only rerendering components when their state has actually changed
- as a front end developer, I would like to simply refer to refer to pieces of data by name (this name could be called a "tag")
    - when constructing a resuable component, I could pass in the strings that indicate the tags that I'm interested in
    - when components are re-rendered the latest value of those tags should be used
    - components should re-render periodically, and only if some constituent tag value has changed
    - tags can be either single point values, or they can be 

Possible implementations

1. periodically push updates from the front end to the back end

TODO
- google "scientific web applications", "client-server data synchronization"


### Backend-frontend datatype synchronization