# Streaming Client Example

This project demonstrates the ability to use real-time Speech Recognition inferencing using Socket.io [client](https://github.com/Open-Speech-EkStep/speech-recognition-open-api-client).

### Setting up example

You need to have a compatible socket.io proxy running https://github.com/Open-Speech-EkStep/speech-recognition-open-api-proxy. 

Change the below mentioned properties in  [examples/react-example/src/App.js](examples/react-example/src/App.js).\


```javascript
streamingURL = '<Add URL to your socket.io proxy HERE>';
punctuateURL = '<Add Punctuate URL to support punctuation>';
```

### Running on Local 

`npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

### Testing with different versions of client

Our client SDK is available as npm package on https://www.npmjs.com/package/@project-sunbird/open-speech-streaming-client. You can point it to specific package in [examples/react-example/package.json](examples/react-example/package.json).
