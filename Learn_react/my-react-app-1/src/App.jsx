import Student from "./students.jsx";

function App() {
  return (
    <div>
      <Student name="abhay" age="30" isStudent={true}/>
      <Student name="ananya" age={40} isStudent={false}/>
      <Student name="Ravi" age={30} isStudent={false}/>
      <Student name="mahesh" age={20} isStudent={true}/>
    </div>
  );
}

export default App
