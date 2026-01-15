import List from "./list"
import List_junk from "./button_list"

function App() {

  const fruits = [
                  {id:1, name:"apple", cal:95}, 
                  {id:2, name:"orange", cal:25},
                  {id:3, name:"banana", cal:44}, 
                  {id:4, name:"coconut", cal:34}, 
                  {id:5, name:"pineapple", cal:64},
                  {id:6, name:"pineapple", cal:100}
              ];

  return (
    <div>
      <List items={fruits} category="Fruits"/>
      <List_junk category="junk_food"/>
    </div>
  )
}

export default App
