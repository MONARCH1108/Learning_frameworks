import React, {useState} from "react";

function FetchDataReddit(){
    const [data, setData]=useState(null)
    const [hasfetched, setHasFetched]=useState(false)
    const [loading, setLoading]=useState(false)
    const [error, setError]=useState(null);

    const GetData=async()=>{
        try{
            setLoading(true);
            setError(null);
            const res = await fetch("http://127.0.0.1:5000/data")
            if(!res.ok){
                throw new Error("API request Failed")
            }
            const json = await res.json();
            setData(json)
            setHasFetched(true)
        }catch(err){
            setError(err.message)
        }finally{
            setLoading(false);
        }
    }

    let content;
    if(loading){
        content="Loading......"
    }else if(error){
        content = error;
    }else if(!data){
        content="No avaible Data"
    }else{
        content=JSON.stringify(data, null, 2)
    }

    return(
        <div>
            <h2>Method-2</h2>
            <button onClick={()=>GetData()}>
                click me
            </button>
            <p>{content}</p>
        </div>
    )
}
export default FetchDataReddit