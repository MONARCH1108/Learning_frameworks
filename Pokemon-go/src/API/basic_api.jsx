function APIHandling(){

    fetch("https://pokeapi.co/api/v2/pokemon/pikachu")
    .then(response => response.json())
    .then(data=>console.log(data))
    //.then(data=>console.log(data.name))
    //.then(data=>console.log(data.weight))
    //.then(data=>console.log(data.id))
    .catch(error => console.log(error))

}
export default APIHandling