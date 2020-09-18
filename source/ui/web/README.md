# Web UI

To run the app:

- enter the react-app directory (`cd react-app`)
- run the react app (`npm start`)
- run electron (`npm run electron`)
- run the Python application #WIP

### React and Electron 

They don't play together, immediately. There are some good resources on this [here](https://jsmanifest.com/create-your-first-react-desktop-application-in-electron-with-hot-reload/) and [here](https://medium.com/@johndyer24/building-a-production-electron-create-react-app-application-with-shared-code-using-electron-builder-c1f70f0e2649).

Preliminary steps for getting them to play together: 

1. Use [Create React App](https://github.com/facebook/create-react-app) bootstrap the base React app
2. Install electron
4. Update scripts section of `package.json` so that the browser doesn't show up when running `npm start`
5. Add command to scripts section of `package.json` to start electron
    - e.g. `"electron": "electron ."`
3. Configure the startup script (`startup.js`) to create the electron window. Add `"main": "src/startup.js"` to package.json. 
1. Install `electron-is-dev`. Use it to tell electron to look at the NodeJS + webpack server (which runs with `npm start`) when in the development context, or `index.html` in the builds folder when in the build context.  

# Typescript

Followed [these instructions](https://create-react-app.dev/docs/adding-typescript/) to add it to the project

Great quick overview of Typescript [here](https://www.typescriptlang.org/docs/handbook/basic-types.html)

Type overview [here](https://www.typescriptlang.org/docs/handbook/basic-types.html)

# electron-quick-start - GENERIC

**Clone and run for a quick way to see Electron in action.**

[Quick Start Guide](https://electronjs.org/docs/tutorial/quick-start) 
