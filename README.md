# Web Client library for Open Speech Streaming API

[![NPM package](https://badgen.net/github/release/Naereen/Strapdown.js)](https://www.npmjs.com/package/@ai4bharat/open-speech-streaming-client)

This package contains the client library to provide real-time streaming functionality for Open Speech API [https://open-speech-ekstep.github.io/asr_model_api/][Open Speech API]. It requires a Socket.io proxy to support it. Details of the proxy can be found https://github.com/Open-Speech-EkStep/speech-recognition-open-api-proxy. 

Visit [Speech Recognititon Streaming API](https://open-speech-ekstep.github.io/asr_streaming_service/) for architecture and other details.

[Open Speech API]: https://open-speech-ekstep.github.io/asr_model_api/

## Table of Contents

- [Getting Started](#getting-started)
- [How to Install](#how-to-install)
- [In Node.js](#in-nodejs)
- [In React Native](#in-react-native)
- [Quick Start](#quick-start)
- [Reference](#reference)
- [Examples](#examples)
- [React Example](#react-example)
- [Getting Help](#getting-help)

## Getting Started

## How to Install

### In Node.js

The preferred way to install the client SDK for Node.js is to use the
[npm](http://npmjs.org) package manager for Node.js. Run the following
into a terminal window:

```sh
npm i @ai4bharat/open-speech-streaming-client
```

### In React Native

To use the client SDK in a react native project, first install the SDK using npm:

```sh
npm i @ai4bharat/open-speech-streaming-client
```

Then within your application, you can reference the react native compatible version of the SDK with the following:

```javascript
import { StreamingClient, SocketStatus } from '@ai4bharat/open-speech-streaming-client';
```

## Quick Start

1. Import the StreamingClient module and create an instance.

    ```javascript

    import {StreamingClient, SocketStatus} from '@ai4bharat/open-speech-streaming-client'

    //Create instance of streaming client.
    const client = new StreamingClient();

    ```

2. Connect to the streaming server with the url and the language required.

    ```javascript


    //Connect to inferencing server
    const inferenceServerURL = '<inferencing-server-url>';
    const language = '<language>';  //(eg: 'en')
    const post_processors = [];

    client.connect(inferenceServerURL, language, post_processors, function (action, id) {
        if (action === SocketStatus.CONNECTED) {
            // Once connection is succesful, start streaming
            client.startStreaming(function (transcript) {
                // transcript will give you the text which can be used further
                console.log('transcript:', transcript);
            }, (e) => {
                console.log("I got error", e);
            })
        } else if (action === SocketStatus.TERMINATED) {
            // Socket is closed and punctuation can be done after it.
        } else {
            //unexpected failures action on connect.
            console.log("Action", action, id);
        }
    })

    ```

3. If punctuation needed in the client sdk, do the following:
[Note: Use this inside the condition block(action === SocketStatus.TERMINATED)]

    ```javascript
    client.punctuateText('<Text to punctuate>', '<punctuation-url>', (status, text) => {
        console.log("Punctuted Text:", text);
    }, (status, error) => {
        console.log("Failed to punctuate", status, error);
    });
    ```

## Reference

SocketStatus has two possible states.`CONNECTED` and `TERMINATED`

------------------------

## Examples

This repo contains samples in examples directory.

### React Example

_Location_: [examples/react-example](examples/react-example)

This example has a React implementation of a streaming client.
You can start example by `npm start` from inside _examples/react-example_.

By default, this examples will point to parent repo as SDK so make sure you have dependencies installed on parent project. You can change to point npm by updating _package.json_

## Getting Help

The best way to interact with our team is through GitHub. Please open an issue in github.
