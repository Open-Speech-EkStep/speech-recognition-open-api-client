## Client library for Open Speech API

This package contains a client lib to provide real-time streaming functionality for Open Speech API [https://open-speech-ekstep.github.io/][Open Speech API].

[Open Speech API]: https://open-speech-ekstep.github.io/


### How to use it

**Step 1: Install the package**

`npm i @project-sunbird/open-speech-streaming-client`

**Step 2: Connect to socket and stream**

```javascript
import {StreamingClient,SocketStatus} from '@project-sunbird/open-speech-streaming-client'

//Create instance of streaming client.
const streamingClient= new StreamingClient();

//Connect to inferencing server
streaming.connect('<inferencing-server-url>', 'en-IN'/* langugaue*/, function (action, id) {
    if (action === SocketStatus.CONNECTED) {
        // Once connection is succesful, start streaming
        streaming.startStreaming(function (transcript) {
            // transcript will give you the text which can be used further
            console.log('transcript:', transcript);
        }, (e) => {
            console.log("I got error", e);
        })
    } else {
        //unexpected failures action on connect.
        console.log("Action", action, id)
    }
})
```

**Punctuation**

You can punctuate a text using the _punctuation_ endpoint. 

```javascript
streaming.punctuateText('Text to punctuate', '<inferencing-server-url>', (status, text) => {
    console.log("Punctuted Text:", text);
}, (status, error) => {
    console.log("Failed to punctuate", status, error);
});
```

**SocketStatus**

SocketStatus has two possible states.`CONNECTED` and `TERMINATED`

