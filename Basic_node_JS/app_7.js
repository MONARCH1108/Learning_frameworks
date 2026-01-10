const EventEmitter = require('events');
const { url } = require('inspector');
const emitter = new EventEmitter();

//Register a listener
emitter.on('messageLogged', (arg) => {
    console.log('Listener called', arg);
})

//Raised an Event
emitter.emit('messageLogged', { id: 1, url: 'http://'});
emitter.emit("messageLogged", { id: 3, url: 'http://hello.com'});


emitter.on("dataBeingSent" , (arg) => {
    console.log("Data sent successfully to ", arg);
})
emitter.emit("dataBeingSent", { id: 1, name: 'Abhay' });
emitter.emit("dataBeingSent", { id: 2, name: 'John' });
