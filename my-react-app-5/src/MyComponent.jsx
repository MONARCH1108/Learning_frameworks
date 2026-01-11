import React, {useState} from 'react';

function MyComponent(){

    const [name, setName] = useState("Guest");
    const [age, setAge] = useState(0)
    const [isEmployed, setIsEmployed] = useState(false)


    const updateName=()=>{
        setName("Abhay Emani")
    }
    const updateAge=()=>{
        setAge(age + 2)
    }
    const updateEmploymentStatus=()=>{
        setIsEmployed(!isEmployed)
    }

    return(
        <div>
            <p>Name: {name} </p>
            <button onClick={updateName}>set Name</button>

            <p>Age: {age} </p>
            <button onClick={updateAge}>set Age</button>

            <p>Employment Status: {isEmployed ? "yes":"no"} </p>
            <button onClick={updateEmploymentStatus}>set Status</button>
        </div>
    )

}
export default MyComponent