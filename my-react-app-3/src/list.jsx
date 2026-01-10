function List(props){

    const itemList = props.items

    //fruits.sort((a, b) => a.name.localeCompare(b.name))
    //fruits.sort((a,b) => b.cal - a.cal)
    
    const lowCalFruits = itemList.filter(items => items.cal < 50)
    const HighCalFruits = itemList.filter(items => items.cal > 50)

    const listItems = HighCalFruits.map(HighCalFruits => 
                <li key={HighCalFruits.id}>{HighCalFruits.name}: <b>{HighCalFruits.cal}</b></li>)
    const listItems_1 = lowCalFruits.map(lowCalFruits => 
                <li key={lowCalFruits.id}>{lowCalFruits.name}: <b>{lowCalFruits.cal}</b></li>)
    return(
        <div>
        <h3>High cal</h3>
        <ul className="fruits">{listItems}</ul>
        <h3>low cal</h3>
        <ul className="fruits">{listItems_1}</ul>
        </div>
    )
}
export default List