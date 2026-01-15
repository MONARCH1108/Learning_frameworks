import React, {useState} from "react"

function Counter(){

    const [count, setCount]=useState(0);

    const increment=()=>{
        setCount(count+1)
    }
    const decrement=()=>{
        setCount(count-1)
    }
    const reset=()=>{
        setCount(0)
    }

    return(
        <div className="Counter_container">
            <p className="count_display">{count}</p>
            <button className="counter_button" onClick={increment}>
                Increment 
            </button>
            <button className="counter_button" onClick={decrement}>
                Decrement
            </button>
            <button className="counter_button" onClick={reset}>
                reset 
            </button>

        </div>
    )

}
export default Counter