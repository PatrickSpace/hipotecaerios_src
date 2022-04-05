const express = require('express');
const path = require('path');

const app = express();
const port = process.env.PORT || 5533;

app.use(express.static('src'));

/*app.get('/', (req, res) => {
  res.send('Hola mundo');
})*/

app.listen(port);
console.log('Server started at http://localhost:' + port)
/*const public = path.join(__dirname, 'src');

// sendFile will go here
app.get('/', function(req, res) {
  res.sendFile(path.join(__dirname, 'src/index2.html'));
});

app.use(express.static(__dirname, 'src'))
app.listen(port);
console.log('Server started at http://localhost:' + port);*/