var http = require('http');
var fs = require('fs');

const recordArtworks = process.argv.length > 2 && process.argv[2] === '1';
if (recordArtworks) {
  try {
    fs.mkdirSync('artworks');
  } catch (e) {
    if (e.code !== 'EEXIST') {
      throw e;
    }
  }
}

var webserver = http.createServer(function (request, response)
{
  if (request.method === 'POST' && request.url === '/artwork') {
    let buffers = [];
    request.on('data', function(chunk) {
      buffers.push(chunk);
    });

    request.on('end', function() {
      if (recordArtworks) {
        const name = new Date().toString();
        const base64String = Buffer.concat(buffers).toString('utf8').replace(/data:image\/png;base64,/, '');
        fs.writeFile(`artworks/${name}.png`, new Buffer(base64String, 'base64'), (e) => console.error);
      }
      response.writeHead(200);
      response.end();
    })
  }
  else {
    fs.readFile('index.html', 'utf-8', function (error, data)
    {
      response.writeHead(200, {'Content-Type': 'text/html'})
      response.end(data);
    });
  }
}).listen(10000);

var io = require('socket.io')(webserver);
console.log("Webserver socket listening on 127.0.0.1:10000");

// ----------------------------------------------------------------------------

const StringDecoder = require('string_decoder').StringDecoder;
const decoder = new StringDecoder('utf8');

// Set up the TCP server to communicate with the game server
const net = require('net');
const gameServer = net.createServer();
const PORT = 8080;
const HOST = '127.0.0.1';
gameServer.listen(PORT, HOST);
console.log(`Game server socket listening on ${HOST}:${PORT}`);

// All this server does is simply relay the information to the web client
let connectedClients = 0
gameServer.on('connection', sock => {
  if (connectedClients > 0) {
    console.log(`Only one game server can be connected at a time, refusing connection from ${sock.remoteAddress}:${sock.remotePort}`);
    return;
  }
  connectedClients++;
  console.log(`Game server connected from ${sock.remoteAddress}:${sock.remotePort}`);
  // Since this is a new client we reset the web interface
  io.sockets.emit('to_client', 'reset\n');

  // What to do when we get data
  sock.on('data', data => {
    io.sockets.emit('to_client', decoder.write(data));
  })

  sock.on('close', () => {
    connectedClients--;
    console.log(`Game server ${sock.remoteAddress}:${sock.remotePort} disconnected`);
  });
});
