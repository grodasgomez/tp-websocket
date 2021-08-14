//Cliente js que se puede ejecutar en el navegador para testear

// Abrimos una conexion
var ws = new WebSocket("ws://127.0.0.1:6789/")

// Definimos el metodo en el cliente que se ejecuta cada vez que el server manda un mensaje
ws.onmessage = function (event) {
  data = JSON.parse(event.data);
  console.log(data)
};

// Envia un mensaje al server
ws.send(JSON.stringify({operation: 1}))