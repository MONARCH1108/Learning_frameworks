const http = require('http');
const server = http.createServer((req, res) => {
    if (req.url === '/') {
        res.write('Hello World');
        res.end();
    }

    if (req.url === '/api/data') {
        res.write(JSON.stringify([1, 2, 3, 4, 5]));
        res.end();
    }
});
server.listen(5000);
console.log('Listening on port 5000...');