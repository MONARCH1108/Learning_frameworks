import { useState } from "react";

function RedditData() {
    const [data, setData] = useState()
    const [hasFetched, setHasFetched] = useState(false);
    
    const GetRedditData=()=>{
        fetch("http://127.0.0.1:5000/data")
        .then( (res) => res.json())
        .then( (json) =>{
            setData(json);
            setHasFetched(true);
            console.log("Data updated in frontend")
        })
    }

    let All_data
    if (!hasFetched) {
        All_data = "Click fetch to load data";
    } else if (data === null || data === undefined) {
        All_data = "No data Available in this call";
    } else {
        All_data = JSON.stringify(data);
    }

    return (
        <div>
            <h2>Method-1</h2>
            <button onClick={()=>GetRedditData()}>Fetch Data</button>
            <p>{All_data}</p>
        </div>
    );
}

export default RedditData;
