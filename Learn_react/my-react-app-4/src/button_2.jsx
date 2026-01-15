function ButtonNew1(){

    const handleClick2=(e)=>console.log(e);
    const handleClick3=(e)=> e.target.textContent = "Hey There";


    return(
        <div>
            <button onClick={(e)=> handleClick2(e)}>Click me for event handler</button>
            <br />
            <button onDoubleClick={(e)=> handleClick3(e)}>Click me for event handler</button>
        </div>
    )
}
export default ButtonNew1