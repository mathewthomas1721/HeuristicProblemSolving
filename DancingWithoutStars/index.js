'use strict'
const app = require('express')();
const bodyParser = require('body-parser');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
const http = require('http').Server(app);
const io = require('socket.io')(http)

let STATE = null; // the current state of the game

// when someone connected, send out the current state
io.on('connection', (socket) => {
  console.log('A connection ' + socket.id + ' established.');
  // send the latest state to the new connector
  io.emit('STATE', STATE);
  socket.on('disconnect', () => {
    console.log('Connection ' + socket.id + ' closed.');
  });
});

app.get('/', (req, res) => {
  // load the webpage
  res.sendFile(__dirname + '/index.html');
});

app.post('/', (req, res) => {
  // update current state
  STATE = req.body;
  // console.log('update state: ', STATE);
  //send state to frontends
  io.emit('STATE', STATE);
  res.sendStatus(200)
});

http.listen(3000, () => {
  console.log('listening on port 3000')
});