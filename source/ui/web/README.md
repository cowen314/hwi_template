# Web UI

To run the app:

- enter the react-app directory (`cd react-app`)
- run the react app (`npm start`)
- run electron (`npm run electron`)
- run the Python application #WIP

### React and Electron 

They don't play together, immediately. There are some good resources on this [here](https://jsmanifest.com/create-your-first-react-desktop-application-in-electron-with-hot-reload/) and [here](https://medium.com/@johndyer24/building-a-production-electron-create-react-app-application-with-shared-code-using-electron-builder-c1f70f0e2649).

Preliminary steps for getting them to play together: 

1. Use create-react-app to configure base React app
2. Install electron
4. Update scripts section of `package.json` so that the browser doesn't show up when running `npm start`
5. Add command to scripts section of `package.json` to start electron
    - e.g. `"electron": "electron ."`
3. Configure the startup script (`startup.js`) to create the electron window. Add `"main": "src/startup.js"` to package.json. 
1. Install `electron-is-dev`. Use it to tell electron to look at the NodeJS + webpack server (which runs with `npm start`) when in the development context, or `index.html` in the builds folder when in the build context.  

---

# electron-quick-start - GENERIC

**Clone and run for a quick way to see Electron in action.**

[Quick Start Guide](https://electronjs.org/docs/tutorial/quick-start) 

**Use this app along with the [Electron API Demos](https://electronjs.org/#get-started) app for API code examples to help you get started.**

A basic Electron application needs just these files:

- `package.json` - Points to the app's main file and lists its details and dependencies.
- `main.js` - Starts the app and creates a browser window to render HTML. This is the app's **main process**.
- `index.html` - A web page to render. This is the app's **renderer process**.

You can learn more about each of these components within the [Quick Start Guide](https://electronjs.org/docs/tutorial/quick-start).

## Resources for Learning Electron

- [electronjs.org/docs](https://electronjs.org/docs) - all of Electron's documentation
- [electronjs.org/community#boilerplates](https://electronjs.org/community#boilerplates) - sample starter apps created by the community
- [electron/electron-quick-start](https://github.com/electron/electron-quick-start) - a very basic starter Electron app
- [electron/simple-samples](https://github.com/electron/simple-samples) - small applications with ideas for taking them further
- [electron/electron-api-demos](https://github.com/electron/electron-api-demos) - an Electron app that teaches you how to use Electron
- [hokein/electron-sample-apps](https://github.com/hokein/electron-sample-apps) - small demo apps for the various Electron APIs

## License

[CC0 1.0 (Public Domain)](LICENSE.md)
