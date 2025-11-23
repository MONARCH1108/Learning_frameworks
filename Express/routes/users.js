import express from 'express';
const router = express.Router()


router.get('/', (req, res)=>{
    res.send('Users Page')
})
router.get('/about', (req, res)=>{
    res.send('About Page')
});
router.post('/', (req, res)=>{
    res.send('to create an User')
})

router
.route('/:id')
.get((req, res)=>{
    console.log(req.user)
    var unit = req.params.id
    res.send(`user with id ${unit}`)
})
.post((req, res)=>{
    var unit = req.params.id
    res.send(`update user with id ${unit}`)
})
.delete((req, res)=>{
    var unit = req.params.id
    res.send(`Delete user with id ${unit}`)
})

const users = [{name: 'abhay'}, {name: 'john'}, {name: 'doe'}]
router.param("id", (req, res, next, id)=>{
    req.user = users[id]
    next()
})

export default router;