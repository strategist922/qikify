// Generated by CoffeeScript 1.3.1
(function() {
  var Forwarder, colors, fs, http, io, zmq;

  io = require('socket.io').listen(8001);

  fs = require('fs');

  http = require('http');

  zmq = require('zmq');

  colors = require('./termcolors.js').colors;

  Forwarder = (function() {

    Forwarder.name = 'Forwarder';

    function Forwarder(name, port, client_socket) {
      this.name = name;
      this.port = port;
      this.client_socket = client_socket;
      this.socket = zmq.socket('sub');
      this.socket.connect('tcp://127.0.0.1:' + this.port.toString());
      this.socket.subscribe('');
    }

    Forwarder.prototype.run = function() {
      var _this = this;
      return this.socket.on('message', function(msg) {
        _this.data = JSON.parse(msg.toString());
        console.log('Recv msg from ' + colors.green(_this.data.name) + colors.none(''));
        return _this.client_socket.emit('message', _this.data);
      });
    };

    return Forwarder;

  })();

  /* Main
  */


  console.log(colors.red('Qikify') + ' *** View Server' + colors.none(''));

  io.on('connection', function(client_socket) {
    var ateSimForwarder, basicForwarder;
    console.log('Qikify *** client has connected');
    client_socket.on('message', function(msg) {
      return console.log('Qikify *** Message received from client: ' + msg);
    });
    ateSimForwarder = new Forwarder('atesim', 5001, client_socket);
    ateSimForwarder.run();
    basicForwarder = new Forwarder('basic', 5002, client_socket);
    return basicForwarder.run();
  });

}).call(this);
