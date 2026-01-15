import GreetingAdvanced from "./greeting_1"

function App() {

  const condition_1 = true
  const condition_2 = false

  return (
    <div>
      <GreetingAdvanced  isLoggedIn={condition_2} username="Ananya"/>
    </div>
  )
}

export default App
