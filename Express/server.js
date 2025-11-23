import express from 'express';
import router from './routes/users.js';

const app = express();

app.set('view engine', 'ejs')

app.get('/', (req, res)=>{
    //res.download('server.js')
    //res.downloadFile('server.js')
    //res.send('Hello World')
    //res.json({name: 'abhay', age: 20})
    res.render('index.ejs', {text:'this is ejs template engine'})
})

app.use('/users', router)

app.listen(3000)
