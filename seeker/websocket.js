const WebSocket = require('ws');
const prompt = require('prompt-sync')
const ws = new WebSocket("wss://localhost:10003/");
ws.onopen = function() {
   ws.send(JSON.stringify({"text":"begin"}));
   ws.send(JSON.stringify({"text": "begin"}));
};

ws.onmessage = function (evt) {
   console.log(JSON.stringify(evt.data));
   ws.send(JSON.stringify({"text": "Hi what is your name?"}));
};
